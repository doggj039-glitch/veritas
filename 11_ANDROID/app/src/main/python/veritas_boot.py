"""Chaquopy boot module for the VERITAS Android app.

MainActivity extracts the bundled VERITAS data tree to the app's files dir once,
then calls run(data_dir, port) on a BACKGROUND thread. We point the engine at that
dir via VERITAS_ROOT (the desktop default path does not exist on a phone), put the
app code on sys.path, and start the same veritas_server the desktop uses — which
then serves m.html (the phone-first UI) over 127.0.0.1.
"""
import os
import sys


def run(data_dir, port=8737):
    os.environ["VERITAS_ROOT"] = str(data_dir)
    app_dir = os.path.join(str(data_dir), "00_APP")
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)          # so `import veritas_server` resolves
    import veritas_server                     # module-level ROOT reads VERITAS_ROOT, sets its own sub-paths
    veritas_server.run(port)                  # blocking serve_forever — runs on the caller's thread
