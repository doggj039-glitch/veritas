# VERITAS — Android (phone-first) build

This is the **Chaquopy + WebView** shell for the phone-first VERITAS. It runs the
**same Python engine** as the desktop (`veritas_server.py`) inside the app and points
a full-screen WebView at **`m.html`**. Built on the phoenix / `app-base` mold, so it
uses the same toolchain that already builds there.

> **You need Android Studio + the Android SDK to build the APK.** Everything else
> (engine, data, UI) is done and proven on the desktop. This folder is the shell +
> the exact steps.

---

## What the app does at runtime
1. On first launch, unzips the bundled `veritas-data.zip` to the phone's private
   files dir → `filesDir/veritas/…` (the desktop project layout).
2. Starts `veritas_server` on a background thread via Chaquopy, with
   `VERITAS_ROOT = filesDir/veritas`, bound to `127.0.0.1:8737`.
3. Loads `http://127.0.0.1:8737/m.html` in the WebView.
4. **Read-aloud** is bridged to the phone's native **TextToSpeech** — `MainActivity`
   overrides the web app's `window.VSpeak()` on every page load. No Piper on Android.

## Why this is light
- The engine uses **only the Python standard library** (`json`, `sqlite3`, `re`,
  `http.server`, `urllib`) — **no pip dependencies**.
- The 89 MB library is now an **on-disk SQLite db** (`VERITAS_definitions_library.db`)
  — queried, never loaded → engine RAM ~44 MB (measured on desktop).
- The phone-first UI (`m.html`) needs **only the library db** — Define/Drift/browse
  read stored data, not the FTS5 corpora. So the bundled data is **~100 MB (LEAN)**.

---

## Build steps
1. **Assemble the data asset** (on a machine with disk space — this desktop is usually
   full, so use the USB or the build box):
   ```
   cd 11_ANDROID
   ./assemble_assets.sh            # LEAN ≈ 100 MB (phone-first)
   #   or  ./assemble_assets.sh --full   # + FTS5 corpora ≈ 280 MB (adds concordance)
   ```
   This writes `app/src/main/assets/veritas-data.zip`.
2. **Open `11_ANDROID/` in Android Studio.** Let it sync Gradle. (If it complains about
   plugin versions, they're pinned in `build.gradle` to the mold's working set:
   AGP 8.1.1, Chaquopy 16.0.0, Kotlin 1.8.21 — bump together to match your installed SDK.)
3. Add a launcher icon (`res/mipmap-*/ic_launcher`) — use the gold-heart VERITAS mark,
   or Android Studio's Image Asset wizard.
4. **Build ▸ Build APK** (or Run on a device). arm64 phones only by default; add
   `armeabi-v7a` in `app/build.gradle` `ndk { abiFilters … }` for old 32-bit devices.

## First run notes
- First launch does the unzip + Python bootstrap → a few seconds of black screen is
  normal; the WebView loads once the engine answers (`MainActivity` polls it).
- When you change the bundled data, re-run `assemble_assets.sh` **and bump
  `assetVersion` in `MainActivity.kt`** so the phone re-extracts it.

---

## Files here
| Path | What |
|---|---|
| `app/src/main/kotlin/law/veritas/app/MainActivity.kt` | WebView + Python start + TTS bridge |
| `app/src/main/python/veritas_boot.py` | sets `VERITAS_ROOT`, imports & runs `veritas_server` |
| `app/src/main/AndroidManifest.xml` | INTERNET perm, cleartext localhost, launcher |
| `app/build.gradle` | Chaquopy config, arm64, no pip deps |
| `build.gradle` / `settings.gradle` | toolchain pinned to the mold |
| `assemble_assets.sh` | builds `veritas-data.zip` (LEAN / `--full`) |

## Not wired yet (only needed if the mobile UI grows)
`m.html` today has **Define · Dictionary · Library · Notes**. If you later add the
desktop-only surfaces to mobile, add the matching bridge:
- **My Sources / PDFs** → `PdfRenderer` or an `ACTION_VIEW` Intent (Android WebView
  has no built-in PDF viewer), + `WebChromeClient.onShowFileChooser` for uploads.
- **Favorites / external links** → `Intent.ACTION_VIEW` to the phone's browser
  (replaces the desktop `/api/open` → xdg-open).
- **Concordance** → bundle with `assemble_assets.sh --full` (the FTS5 corpora).

## The engine changes that made this possible (already in the desktop tree)
- `VERITAS_ROOT` env var in `veritas_server.py`, `blackletter_gate.py`,
  `blackletter_usage.py` (default = desktop path, so desktop is unchanged).
- `veritas_server.run(port)` — a callable entry point (not just CLI `__main__`).
- `build_library_db.py` + `SqliteEntries` — the library → on-disk SQLite conversion.
