"""Command line.

    python -m p009 record      start recording (Windows) and open the dashboard
    python -m p009 view        open the dashboard without recording
    python -m p009 simulate    offline policy comparison (pilot|final)
"""
import argparse
import secrets
import socket
import sys
import threading
import webbrowser

from p009.store import Store, default_folder


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _serve(store, recorder, open_browser):
    import uvicorn

    from p009.api import create_app
    token = secrets.token_urlsafe(32)
    port = _free_port()
    url = f"http://127.0.0.1:{port}/#token={token}"
    print(f"\nDashboard (this link works only on this computer, only while this window is open):\n  {url}\n")
    if open_browser:
        threading.Timer(1.5, webbrowser.open, (url,)).start()
    uvicorn.run(create_app(store, token, recorder), host="127.0.0.1", port=port, log_level="warning")


def _store(args):
    from p009.protect import DPAPIProtector
    return Store(args.folder or default_folder(), DPAPIProtector(), args.retention_days, args.max_gb * 1024 ** 3)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="p009")
    parser.add_argument("command", choices=["record", "view", "simulate"])
    parser.add_argument("mode", nargs="?", default="pilot", help="simulate: pilot or final")
    parser.add_argument("--folder", help="data folder (default %%LOCALAPPDATA%%\\P009ScreenMemory)")
    parser.add_argument("--retention-days", type=int, default=7)
    parser.add_argument("--max-gb", type=float, default=2.0)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--exclude-program", action="append", default=[])
    parser.add_argument("--exclude-title", action="append", default=[])
    args = parser.parse_args(argv)

    if args.command == "simulate":
        from p009 import simulate
        simulate.main(["simulate", args.mode])
        return 0

    if sys.platform != "win32":
        print("Recording and viewing are only implemented for Windows.")
        return 2
    store = _store(args)

    if args.command == "view":
        _serve(store, None, not args.no_browser)
        return 0

    print("Screen Memory will save images of the window you are using, every time something")
    print("meaningful changes, encrypted in your Windows account, for", args.retention_days, "days.")
    print("Password managers, private browsing and sign-in or banking pages are skipped.")
    print("Only record your own screen. Pause or delete at any time from the dashboard.")
    if input("Start recording? Type yes: ").strip().lower() != "yes":
        print("Not started.")
        return 1

    from p009 import platform_win
    from p009.exclusions import Exclusions
    from p009.recorder import Recorder
    platform_win.dpi_aware()
    recorder = Recorder(store, platform_win, Exclusions(args.exclude_program, args.exclude_title))
    stop = threading.Event()
    worker = threading.Thread(target=recorder.run, args=(stop,), daemon=True)
    worker.start()
    try:
        _serve(store, recorder, not args.no_browser)
    finally:
        stop.set()
        worker.join(timeout=5)
        print("Recording stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
