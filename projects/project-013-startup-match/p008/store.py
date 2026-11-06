"""SQLite storage and accounts.

Passwords: scrypt with a per-user salt (standard library). Sessions: random tokens, stored
only as SHA-256 hashes, expiring after 7 days. Every query is parameterised.
"""
import hashlib
import hmac
import json
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone

from p008.matching import Deal, Investor, Startup

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, role TEXT NOT NULL CHECK (role IN ('founder','investor')),
    salt BLOB NOT NULL, pw_hash BLOB NOT NULL, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE, expires TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS startups (id INTEGER PRIMARY KEY, owner_id INTEGER UNIQUE NOT NULL REFERENCES users ON DELETE CASCADE,
    name TEXT NOT NULL, one_liner TEXT NOT NULL DEFAULT '', sector TEXT, stage TEXT, country TEXT, raising INTEGER,
    contact TEXT NOT NULL DEFAULT '', listed INTEGER NOT NULL DEFAULT 1, updated TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS investors (id INTEGER PRIMARY KEY, owner_id INTEGER UNIQUE NOT NULL REFERENCES users ON DELETE CASCADE,
    name TEXT NOT NULL, sectors TEXT NOT NULL DEFAULT '[]', stages TEXT NOT NULL DEFAULT '[]', countries TEXT NOT NULL DEFAULT '[]',
    check_min INTEGER, check_max INTEGER, contact TEXT NOT NULL DEFAULT '', updated TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS deals (id INTEGER PRIMARY KEY, investor_id INTEGER NOT NULL REFERENCES investors ON DELETE CASCADE,
    company TEXT NOT NULL, sector TEXT NOT NULL, stage TEXT NOT NULL, on_date TEXT NOT NULL, source TEXT NOT NULL, verified TEXT);
CREATE TABLE IF NOT EXISTS intros (id INTEGER PRIMARY KEY, startup_id INTEGER NOT NULL REFERENCES startups ON DELETE CASCADE,
    investor_id INTEGER NOT NULL REFERENCES investors ON DELETE CASCADE, message TEXT NOT NULL, status TEXT NOT NULL,
    created TEXT NOT NULL, updated TEXT NOT NULL);
CREATE UNIQUE INDEX IF NOT EXISTS one_open_intro ON intros (startup_id, investor_id) WHERE status IN ('requested', 'accepted', 'in-talks');
CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, intro_id INTEGER NOT NULL REFERENCES intros ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES users, text TEXT NOT NULL, at TEXT NOT NULL);
"""

SESSION_DAYS = 7


def now():
    return datetime.now(timezone.utc)


class StoreError(Exception):
    pass


class Store:
    def __init__(self, path):
        self.path = str(path)
        with self.db() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def db(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    # ---------- accounts ----------

    @staticmethod
    def _hash(password, salt):
        return hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    def register(self, email, password, role):
        if len(password) < 10:
            raise StoreError("Use a password of at least 10 characters.")
        salt = secrets.token_bytes(16)
        try:
            with self.db() as db:
                cur = db.execute("INSERT INTO users (email, role, salt, pw_hash, created) VALUES (?, ?, ?, ?, ?)",
                                 (email.strip().lower(), role, salt, self._hash(password, salt), now().isoformat()))
                return cur.lastrowid
        except sqlite3.IntegrityError as exc:
            raise StoreError("An account with that e-mail already exists.") from exc

    def check_password(self, email, password):
        with self.db() as db:
            row = db.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
        # Hash even for unknown e-mails, so timing does not reveal who has an account.
        salt = row["salt"] if row else b"\0" * 16
        ok = hmac.compare_digest(self._hash(password, salt), row["pw_hash"] if row else b"\0" * 32)
        return dict(row) if row and ok else None

    def new_session(self, user_id):
        token = secrets.token_urlsafe(32)
        with self.db() as db:
            db.execute("INSERT INTO sessions VALUES (?, ?, ?)", (hashlib.sha256(token.encode()).hexdigest(), user_id,
                                                                  (now() + timedelta(days=SESSION_DAYS)).isoformat()))
        return token

    def user_for(self, token):
        if not token:
            return None
        with self.db() as db:
            row = db.execute("SELECT u.id, u.email, u.role, s.expires FROM sessions s JOIN users u ON u.id = s.user_id "
                             "WHERE s.token_hash = ?", (hashlib.sha256(token.encode()).hexdigest(),)).fetchone()
        if not row or datetime.fromisoformat(row["expires"]) < now():
            return None
        return dict(row)

    def end_session(self, token):
        with self.db() as db:
            db.execute("DELETE FROM sessions WHERE token_hash = ?", (hashlib.sha256(token.encode()).hexdigest(),))

    # ---------- profiles ----------

    def save_startup(self, owner_id, p, today=None):
        today = (today or date.today()).isoformat()
        with self.db() as db:
            db.execute("INSERT INTO startups (owner_id, name, one_liner, sector, stage, country, raising, contact, listed, updated) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (owner_id) DO UPDATE SET name = excluded.name, "
                       "one_liner = excluded.one_liner, sector = excluded.sector, stage = excluded.stage, country = excluded.country, "
                       "raising = excluded.raising, contact = excluded.contact, listed = excluded.listed, updated = excluded.updated",
                       (owner_id, p["name"], p.get("one_liner", ""), p.get("sector"), p.get("stage"), p.get("country"),
                        p.get("raising"), p.get("contact", ""), int(p.get("listed", True)), today))

    def save_investor(self, owner_id, p, today=None):
        today = (today or date.today()).isoformat()
        with self.db() as db:
            db.execute("INSERT INTO investors (owner_id, name, sectors, stages, countries, check_min, check_max, contact, updated) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (owner_id) DO UPDATE SET name = excluded.name, "
                       "sectors = excluded.sectors, stages = excluded.stages, countries = excluded.countries, "
                       "check_min = excluded.check_min, check_max = excluded.check_max, contact = excluded.contact, updated = excluded.updated",
                       (owner_id, p["name"], json.dumps(p.get("sectors", [])), json.dumps(p.get("stages", [])),
                        json.dumps(p.get("countries", [])), p.get("check_min"), p.get("check_max"), p.get("contact", ""), today))

    def startup_row(self, owner_id=None, startup_id=None):
        with self.db() as db:
            q, arg = ("owner_id", owner_id) if owner_id is not None else ("id", startup_id)
            r = db.execute(f"SELECT * FROM startups WHERE {q} = ?", (arg,)).fetchone()
        return dict(r) if r else None

    def investor_row(self, owner_id=None, investor_id=None):
        with self.db() as db:
            q, arg = ("owner_id", owner_id) if owner_id is not None else ("id", investor_id)
            r = db.execute(f"SELECT * FROM investors WHERE {q} = ?", (arg,)).fetchone()
        if not r:
            return None
        d = dict(r)
        for k in ("sectors", "stages", "countries"):
            d[k] = json.loads(d[k])
        with self.db() as db:
            d["deals"] = [dict(x) for x in db.execute("SELECT * FROM deals WHERE investor_id = ? ORDER BY on_date DESC", (d["id"],))]
        return d

    def add_deal(self, investor_id, deal):
        with self.db() as db:
            return db.execute("INSERT INTO deals (investor_id, company, sector, stage, on_date, source, verified) VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (investor_id, deal["company"], deal["sector"], deal["stage"], deal["on_date"], deal["source"],
                               deal.get("verified"))).lastrowid

    def delete_deal(self, investor_id, deal_id):
        with self.db() as db:
            return db.execute("DELETE FROM deals WHERE id = ? AND investor_id = ?", (deal_id, investor_id)).rowcount

    def all_investors(self):
        with self.db() as db:
            ids = [r["owner_id"] for r in db.execute("SELECT owner_id FROM investors")]
        return [self.investor_row(owner_id=i) for i in ids]

    def listed_startups(self):
        with self.db() as db:
            return [dict(r) for r in db.execute("SELECT * FROM startups WHERE listed = 1")]

    # ---------- intros and messages ----------

    def create_intro(self, startup_id, investor_id, message, daily_limit=10):
        stamp = now().isoformat()
        since = (now() - timedelta(days=1)).isoformat()
        with self.db() as db:
            recent = db.execute("SELECT COUNT(*) FROM intros WHERE startup_id = ? AND created >= ?", (startup_id, since)).fetchone()[0]
            if recent >= daily_limit:
                raise StoreError(f"You can send at most {daily_limit} intro requests a day.")
            try:
                return db.execute("INSERT INTO intros (startup_id, investor_id, message, status, created, updated) VALUES (?, ?, ?, 'requested', ?, ?)",
                                  (startup_id, investor_id, message, stamp, stamp)).lastrowid
            except sqlite3.IntegrityError as exc:
                raise StoreError("You already have an open intro with this investor.") from exc

    def intro(self, intro_id):
        with self.db() as db:
            r = db.execute("SELECT i.*, s.owner_id AS founder_id, v.owner_id AS investor_owner_id, s.name AS startup_name, "
                           "v.name AS investor_name, s.contact AS startup_contact, v.contact AS investor_contact "
                           "FROM intros i JOIN startups s ON s.id = i.startup_id JOIN investors v ON v.id = i.investor_id WHERE i.id = ?",
                           (intro_id,)).fetchone()
        return dict(r) if r else None

    def intros_for(self, user_id):
        with self.db() as db:
            ids = [r[0] for r in db.execute("SELECT i.id FROM intros i JOIN startups s ON s.id = i.startup_id JOIN investors v ON v.id = i.investor_id "
                                            "WHERE s.owner_id = ? OR v.owner_id = ? ORDER BY i.updated DESC", (user_id, user_id))]
        return [self.intro(i) for i in ids]

    def set_intro_status(self, intro_id, status):
        with self.db() as db:
            db.execute("UPDATE intros SET status = ?, updated = ? WHERE id = ?", (status, now().isoformat(), intro_id))

    def add_message(self, intro_id, author_id, text):
        with self.db() as db:
            db.execute("INSERT INTO messages (intro_id, author_id, text, at) VALUES (?, ?, ?, ?)", (intro_id, author_id, text, now().isoformat()))
            db.execute("UPDATE intros SET updated = ? WHERE id = ?", (now().isoformat(), intro_id))

    def messages(self, intro_id):
        with self.db() as db:
            return [dict(r) for r in db.execute("SELECT m.*, u.role AS author_role FROM messages m JOIN users u ON u.id = m.author_id "
                                                "WHERE intro_id = ? ORDER BY m.id", (intro_id,))]


def as_startup(row) -> Startup:
    return Startup(row["id"], row["name"], row["sector"], row["stage"], row["country"], row["raising"], date.fromisoformat(row["updated"]))


def as_investor(row) -> Investor:
    deals = tuple(Deal(d["company"], d["sector"], d["stage"], date.fromisoformat(d["on_date"]), d["source"],
                       date.fromisoformat(d["verified"]) if d["verified"] else None) for d in row["deals"])
    return Investor(row["id"], row["name"], tuple(row["sectors"]), tuple(row["stages"]), tuple(row["countries"]),
                    row["check_min"], row["check_max"], deals, date.fromisoformat(row["updated"]))
