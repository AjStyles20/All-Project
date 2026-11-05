"""python -m p011 [--db PATH]   or   python -m p011 evaluate final"""
import argparse
import secrets
import socket
import sys
import threading
import webbrowser


def main(argv=None):
    parser = argparse.ArgumentParser(prog="p011")
    parser.add_argument("command", nargs="?", default="serve", choices=["serve", "evaluate"])
    parser.add_argument("mode", nargs="?", default="pilot")
    parser.add_argument("--db", default="defence_practice.sqlite3")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "evaluate":
        from p011 import evaluation
        evaluation.main(["evaluate", args.mode])
        return 0
    import uvicorn

    from p011.app import create_app
    token = secrets.token_urlsafe(32)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    url = f"http://127.0.0.1:{port}/#token={token}"
    print(f"\nOpen (only on this computer, while this window is open):\n  {url}\n")
    if not args.no_browser:
        threading.Timer(1.5, webbrowser.open, (url,)).start()
    uvicorn.run(create_app(args.db, token), host="127.0.0.1", port=port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
