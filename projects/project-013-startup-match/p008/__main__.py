"""python -m p008 [--db PATH] [--port 8019]          run the app on 127.0.0.1
   python -m p008 seed [--db PATH]                    add fictional demo profiles (a random demo password is printed once)
"""
import argparse
import secrets
import sys
from datetime import date, timedelta


def seed(db_path):
    from p008.store import Store, StoreError
    store = Store(db_path)
    password = "demo-" + secrets.token_urlsafe(9)
    today = date.today()
    founders = [
        ("lumen@demo.test", {"name": "Lumen Ledger (fictional)", "one_liner": "Bookkeeping for market traders", "sector": "fintech",
                             "stage": "seed", "country": "NG", "raising": 800000, "contact": "founders@lumen.demo.test"}),
        ("tidepool@demo.test", {"name": "Tidepool Tutor (fictional)", "one_liner": "Offline maths practice on cheap phones",
                                "sector": "education", "stage": "pre-seed", "country": "KE", "raising": 250000, "contact": "hi@tidepool.demo.test"}),
    ]
    investors = [
        ("harbour@demo.test", {"name": "Harbour Seed Fund (fictional)", "sectors": ["fintech", "logistics"], "stages": ["pre-seed", "seed"],
                               "countries": ["NG", "GH", "KE"], "check_min": 50000, "check_max": 300000, "contact": "deals@harbour.demo.test"},
         [("Kola Pay", "fintech", "seed", 200), ("Routewise", "logistics", "seed", 400), ("Ajo Box", "fintech", "pre-seed", 600)]),
        ("northwind@demo.test", {"name": "Northwind Ventures (fictional)", "sectors": ["education", "health"], "stages": ["seed"],
                                 "countries": ["KE", "UG"], "check_min": 100000, "check_max": 500000, "contact": "team@northwind.demo.test"},
         [("Medly", "health", "series-a", 100), ("Classly", "education", "series-a", 250), ("CareLoop", "health", "series-a", 300),
          ("Vitals", "health", "series-b", 500)]),
    ]
    made = 0
    for email, profile in founders:
        try:
            uid = store.register(email, password, "founder")
            store.save_startup(uid, profile, today)
            made += 1
        except StoreError:
            pass
    for email, profile, deals in investors:
        try:
            uid = store.register(email, password, "investor")
        except StoreError:
            continue
        store.save_investor(uid, profile, today)
        inv = store.investor_row(owner_id=uid)
        for company, sector, stage, days in deals:
            store.add_deal(inv["id"], {"company": company + " (fictional)", "sector": sector, "stage": stage,
                                       "on_date": (today - timedelta(days=days)).isoformat(), "source": "Demo data",
                                       "verified": (today - timedelta(days=30)).isoformat() if days < 300 else None})
        made += 1
    print(f"Added {made} fictional demo accounts: " + ", ".join(e for e, *_ in founders + investors))
    print(f"Demo password for all of them (this run only): {password}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="p008")
    parser.add_argument("command", nargs="?", default="serve", choices=["serve", "seed"])
    parser.add_argument("--db", default="startupmatch.sqlite3")
    parser.add_argument("--port", type=int, default=8019)
    args = parser.parse_args(argv)
    if args.command == "seed":
        seed(args.db)
        return 0
    import uvicorn

    from p008.app import create_app
    print(f"StartupMatch on http://127.0.0.1:{args.port}")
    uvicorn.run(create_app(args.db), host="127.0.0.1", port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
