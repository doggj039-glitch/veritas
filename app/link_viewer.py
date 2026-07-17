"""
VERITAS -- link_viewer.py

A native window (Qt Widgets). Click Fetch on ANY link and it just works:

  * Normal sites  -> fast download (requests), no browser.
  * Blocked sites (congress.gov, JS-built pages) -> the app quietly loads the
    page with a background browser engine, so it works the same way Firefox
    does -- one click, no copy/paste.

The middle box always shows exactly the text that will be saved. You can also
paste text there manually (from Firefox) if you ever want to.

  * Save is the ONLY thing that stores the page (never automatic).
  * NO paid API, ever. The only network is fetching the page you asked for.
  * Every saved file keeps SOURCE URL + DATE SAVED (via page_cleaner).

Run:
    python link_viewer.py
    python link_viewer.py "https://a-link"
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal, QTimer, QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QPlainTextEdit, QLabel, QMessageBox,
)

# QtWebEngine MUST be imported before a QApplication is created -- so import it
# here at module load (before open_link makes the app). Used only as the
# fallback that loads sites which block the plain fetch (e.g. congress.gov).
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    _HAS_WEBENGINE = True
except Exception:
    QWebEngineView = None
    _HAS_WEBENGINE = False

sys.path.insert(0, str(Path(__file__).resolve().parent))
import page_cleaner  # noqa: E402

SAVED_DIR = Path(__file__).resolve().parent.parent / "saved_sources"


def _title_from_url(url: str) -> str:
    tail = re.sub(r"[?#].*$", "", url.rstrip("/")).rsplit("/", 1)[-1]
    tail = re.sub(r"\.\w+$", "", tail).replace("-", " ").replace("_", " ").strip()
    return tail or (url.split("//")[-1].split("/")[0] if "//" in url else "saved page")


class FetchWorker(QThread):
    """Fast fetch + clean off the UI thread (requests). Signals 'blocked' if the
    site refuses a plain download, so the window can retry with a real browser."""
    done = pyqtSignal(dict)
    blocked = pyqtSignal(str, str)          # url, reason

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            self.done.emit(page_cleaner.clean_url(self.url))
        except Exception as exc:
            self.blocked.emit(self.url, f"{type(exc).__name__}: {exc}")


class LinkViewer(QMainWindow):
    def __init__(self, url: str = ""):
        super().__init__()
        self.fetched_title: str | None = None
        self.worker: FetchWorker | None = None
        self._bview = None                  # background browser view (lazy)
        self._btimer = None
        self._bdone = True
        self.setWindowTitle("VERITAS -- Source Saver")
        self.resize(940, 760)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        row = QHBoxLayout()
        self.url_in = QLineEdit(url)
        self.url_in.setPlaceholderText("Paste a link, e.g. https://www.congress.gov/bill/…")
        self.url_in.returnPressed.connect(self.fetch)
        self.url_in.textChanged.connect(self._refresh_save)
        fetch_btn = QPushButton("Fetch")
        fetch_btn.clicked.connect(self.fetch)
        row.addWidget(QLabel("Link:"))
        row.addWidget(self.url_in, 1)
        row.addWidget(fetch_btn)
        layout.addLayout(row)

        self.preview = QPlainTextEdit()
        self.preview.setPlaceholderText("The cleaned page text appears here after Fetch.")
        self.preview.textChanged.connect(self._refresh_save)
        layout.addWidget(self.preview, 1)

        act = QHBoxLayout()
        self.save_btn = QPushButton("Save This Page")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        self.status = QLabel(" ")
        act.addWidget(self.save_btn)
        act.addWidget(close_btn)
        act.addStretch(1)
        act.addWidget(self.status)
        layout.addLayout(act)

        if url.strip():
            self.fetch()

    def _refresh_save(self):
        self.save_btn.setEnabled(
            bool(self.preview.toPlainText().strip()) and bool(self.url_in.text().strip()))

    # --- Fetch: fast path first ---
    def fetch(self):
        url = self.url_in.text().strip()
        if not url:
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            self.url_in.setText(url)
        self.fetched_title = None
        self.status.setText("Fetching…")
        self.preview.setPlainText("")
        self.worker = FetchWorker(url)
        self.worker.done.connect(self._on_fast_done)
        self.worker.blocked.connect(lambda u, r: self._browser_fetch(u))
        self.worker.start()

    def _on_fast_done(self, result: dict):
        if result.get("kept_chars", 0) > 0:
            self._populate(result)
        else:
            # empty (JS-built page) -> let the real browser render it
            self._browser_fetch(result.get("url") or self.url_in.text().strip())

    # --- Fetch: browser fallback (only when the fast path is blocked/empty) ---
    def _browser_fetch(self, url: str):
        self.status.setText("Site blocked the quick fetch — loading it in the background browser…")
        if not _HAS_WEBENGINE:
            self._soft_fail("This site needs the browser engine, which isn't installed. "
                            "You can still paste the page text into the box and Save.")
            return
        self._bdone = False
        self._bview = QWebEngineView()          # hidden; never shown
        self._btimer = QTimer(self)
        self._btimer.setSingleShot(True)
        self._btimer.timeout.connect(lambda: self._browser_finished(False, url))
        self._btimer.start(40000)
        self._bview.loadFinished.connect(lambda ok: self._browser_finished(ok, url))
        self._bview.load(QUrl(url))

    def _browser_finished(self, ok: bool, url: str):
        if self._bdone:
            return
        self._bdone = True
        if self._btimer:
            self._btimer.stop()
        if not ok:
            self._soft_fail("The background browser couldn't load this page (or it timed out).")
            return
        self._bview.page().toHtml(lambda html: self._browser_html(html, url))

    def _browser_html(self, html: str, url: str):
        try:
            result = page_cleaner.clean_html(html, url)
            result["url"] = url
            if result.get("kept_chars", 0) > 0:
                self._populate(result)
            else:
                self._soft_fail("Loaded the page but found no readable text.")
        except Exception as exc:
            self._soft_fail(f"Could not clean the page: {exc}")

    # --- shared ---
    def _populate(self, result: dict):
        kept = result.get("kept_chars", 0)
        self.fetched_title = result.get("title")
        self.preview.setPlainText(result.get("text", ""))
        self.status.setText(f"Fetched ({kept:,} chars). Review, then Save.")

    def _soft_fail(self, msg: str):
        self.status.setText(msg)

    # --- Save (only on click; fetched or pasted) ---
    def save(self):
        text = self.preview.toPlainText().strip()
        url = self.url_in.text().strip()
        if not text:
            return
        if not url:
            QMessageBox.warning(self, "Add the link",
                                "Put the source URL in the top box so the save keeps its provenance.")
            return
        try:
            looks_html = ("</" in text or "/>" in text) and "<" in text and ">" in text
            if looks_html:
                result = page_cleaner.clean_html(text, url)
            else:
                result = {"title": self.fetched_title or _title_from_url(url),
                          "text": text, "kept_chars": len(text)}
            path = page_cleaner.save_cleaned(result, url, SAVED_DIR)
            self.status.setText(f"Saved → {path.name}")
            QMessageBox.information(
                self, "Saved",
                f"Saved to:\n{path}\n\nKept {result.get('kept_chars', 0):,} chars.\n"
                f"Source URL and date saved are stored with it.")
        except Exception as exc:
            QMessageBox.warning(self, "Save failed", f"Could not save:\n{exc}")


def open_link(url: str = ""):
    if QApplication.instance() is None:
        # required for QtWebEngine to share the GL context cleanly
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = LinkViewer(url)
    window.show()
    app.exec()


if __name__ == "__main__":
    open_link(sys.argv[1] if len(sys.argv) > 1 else "")
