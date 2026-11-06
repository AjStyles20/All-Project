"""Command line.

    python -m p005 analyse app.log db.log --report incident.html --session incident.p005.json
    python -m p005 record incident.p005.json --hypothesis db_pool --result confirms \\
        --check "max_connections reached at 10:14 in pg_stat_activity" --by "AJ"
    python -m p005 demo ambiguous --out demo.log      # write a synthetic incident to try it on
"""
import argparse
import sys
from pathlib import Path

from p005 import report
from p005.diagnose import diagnose
from p005.logs import read_all


def analyse(paths, report_path, session_path):
    events, skipped = read_all(paths)
    d = diagnose(events)
    if session_path and Path(session_path).exists():
        session = report.load(session_path)
    else:
        session = report.new_session(paths, d)
    report.apply_checks(d, session)
    if session_path:
        report.save(session_path, session)
    if report_path:
        Path(report_path).write_text(report.html_report(d, session), encoding="utf-8")
    print(report.text_summary(d))
    unread = {k: v for k, v in skipped.items() if v}
    if unread:
        print("\nLines not understood (skipped): " + ", ".join(f"{k}: {v}" for k, v in unread.items()))
    return d


def main(argv=None):
    parser = argparse.ArgumentParser(prog="p005")
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("analyse", help="diagnose log files")
    a.add_argument("logs", nargs="+")
    a.add_argument("--report", help="write an HTML report here")
    a.add_argument("--session", help="session file for recorded checks")
    r = sub.add_parser("record", help="record the result of a check you ran")
    r.add_argument("session")
    r.add_argument("--hypothesis", required=True)
    r.add_argument("--result", required=True, choices=["confirms", "refutes"])
    r.add_argument("--check", required=True, help="what you checked and what you saw")
    r.add_argument("--by", required=True)
    g = sub.add_parser("demo", help="write a synthetic incident log")
    g.add_argument("kind", choices=["clear", "red_herring", "ambiguous", "missing"])
    g.add_argument("--seed", type=int, default=1)
    g.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        if args.command == "analyse":
            analyse(args.logs, args.report, args.session)
        elif args.command == "record":
            session = report.load(args.session)
            report.record(session, args.hypothesis, args.check, args.result, args.by)
            report.save(args.session, session)
            print(f"Recorded. Run analyse again with --session {args.session} to update the report.")
        else:
            from p005.benchmark import generate
            lines, truth = generate(args.kind, args.seed)
            Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"Wrote {len(lines)} synthetic lines to {args.out} (synthetic; the injected cause is hidden on purpose).")
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
