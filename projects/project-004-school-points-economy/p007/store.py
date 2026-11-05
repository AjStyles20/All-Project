"""SQLite ledger. Each function opens its own connection; writes are single transactions.

Balances are derived from the transaction log, never stored, so they cannot drift.
"""
import sqlite3
import uuid
from contextlib import contextmanager

from p007.domain import (Action, Dataset, IssuerContext, RewardItem, RewardPolicy,
                         RewardTransaction, StudentContext)

SCHEMA = """
CREATE TABLE IF NOT EXISTS policies (
    policy_id TEXT PRIMARY KEY, version INTEGER NOT NULL, name TEXT NOT NULL, category TEXT NOT NULL,
    earning_rule TEXT NOT NULL, intended_objective TEXT NOT NULL,
    points_per_award INTEGER NOT NULL CHECK (points_per_award > 0), objective_measure TEXT);
CREATE TABLE IF NOT EXISTS students (student_id TEXT PRIMARY KEY, group_label TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS issuers (issuer_id TEXT PRIMARY KEY, role TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS issuer_scope (
    issuer_id TEXT NOT NULL REFERENCES issuers, policy_id TEXT NOT NULL REFERENCES policies,
    PRIMARY KEY (issuer_id, policy_id));
CREATE TABLE IF NOT EXISTS opportunities (
    student_id TEXT NOT NULL REFERENCES students, policy_id TEXT NOT NULL REFERENCES policies,
    issuer_id TEXT NOT NULL REFERENCES issuers, count INTEGER CHECK (count IS NULL OR count >= 0),
    PRIMARY KEY (student_id, policy_id, issuer_id));
CREATE TABLE IF NOT EXISTS rewards (
    reward_id TEXT PRIMARY KEY, name TEXT NOT NULL, point_cost INTEGER NOT NULL CHECK (point_cost > 0),
    stock INTEGER NOT NULL CHECK (stock >= 0));
CREATE TABLE IF NOT EXISTS transactions (
    seq INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id TEXT UNIQUE NOT NULL,
    student_id TEXT NOT NULL REFERENCES students, issuer_id TEXT, policy_id TEXT, policy_version INTEGER,
    action TEXT NOT NULL CHECK (action IN ('EARN', 'REDEEM', 'REVERSE')), category TEXT NOT NULL,
    amount INTEGER NOT NULL, reason_code TEXT NOT NULL, timestamp INTEGER NOT NULL, measure REAL,
    reverses TEXT UNIQUE REFERENCES transactions (transaction_id));
"""


class LedgerError(Exception):
    """A refused ledger operation. The message is safe to show to the user."""


class Ledger:
    def __init__(self, path):
        self.path = str(path)
        with self._connect() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, isolation_level=None)
        db.execute("PRAGMA foreign_keys = ON")
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def _write(self):
        # BEGIN IMMEDIATE takes the write lock first, so a balance check and the spend that
        # depends on it cannot interleave with another redemption.
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                yield db
                db.execute("COMMIT")
            except BaseException:
                db.execute("ROLLBACK")
                raise

    # ---- setup ----

    def add_policy(self, policy: RewardPolicy) -> None:
        with self._write() as db:
            db.execute("INSERT INTO policies VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (policy.policy_id, policy.version, policy.name, policy.category, policy.earning_rule,
                        policy.intended_objective, policy.points_per_award, policy.objective_measure))

    def add_student(self, student_id: str, group: str) -> None:
        with self._write() as db:
            db.execute("INSERT INTO students VALUES (?, ?)", (student_id, group))

    def add_issuer(self, issuer: IssuerContext) -> None:
        with self._write() as db:
            db.execute("INSERT INTO issuers VALUES (?, ?)", (issuer.issuer_id, issuer.role))
            db.executemany("INSERT INTO issuer_scope VALUES (?, ?)",
                           [(issuer.issuer_id, p) for p in sorted(issuer.policy_scope)])

    def set_opportunities(self, student_id: str, policy_id: str, issuer_id: str, count: int | None) -> None:
        with self._write() as db:
            db.execute("INSERT INTO opportunities VALUES (?, ?, ?, ?) ON CONFLICT DO UPDATE SET count = excluded.count",
                       (student_id, policy_id, issuer_id, count))

    def add_reward(self, item: RewardItem) -> None:
        with self._write() as db:
            db.execute("INSERT INTO rewards VALUES (?, ?, ?, ?)", (item.reward_id, item.name, item.point_cost, item.stock))

    # ---- operations ----

    def earn(self, issuer_id: str, student_id: str, policy_id: str, timestamp: int,
             measure: float | None = None, reason_code: str = "AWARD") -> str:
        with self._write() as db:
            policy = db.execute("SELECT * FROM policies WHERE policy_id = ?", (policy_id,)).fetchone()
            if policy is None:
                raise LedgerError("Unknown policy.")
            if db.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,)).fetchone() is None:
                raise LedgerError("Unknown student.")
            if db.execute("SELECT 1 FROM issuer_scope WHERE issuer_id = ? AND policy_id = ?",
                          (issuer_id, policy_id)).fetchone() is None:
                raise LedgerError("This issuer may not award points under this policy.")
            if policy["objective_measure"] and measure is None:
                raise LedgerError(f"This policy needs the {policy['objective_measure']} for each award.")
            transaction_id = uuid.uuid4().hex
            db.execute("INSERT INTO transactions (transaction_id, student_id, issuer_id, policy_id, policy_version, "
                       "action, category, amount, reason_code, timestamp, measure) VALUES (?, ?, ?, ?, ?, 'EARN', ?, ?, ?, ?, ?)",
                       (transaction_id, student_id, issuer_id, policy_id, policy["version"], policy["category"],
                        policy["points_per_award"], reason_code, timestamp, measure))
            return transaction_id

    def redeem(self, student_id: str, reward_id: str, timestamp: int) -> str:
        with self._write() as db:
            item = db.execute("SELECT * FROM rewards WHERE reward_id = ?", (reward_id,)).fetchone()
            if item is None:
                raise LedgerError("Unknown reward.")
            if item["stock"] < 1:
                raise LedgerError("That reward is out of stock.")
            if self._balance(db, student_id) < item["point_cost"]:
                raise LedgerError("Not enough points.")
            db.execute("UPDATE rewards SET stock = stock - 1 WHERE reward_id = ?", (reward_id,))
            transaction_id = uuid.uuid4().hex
            db.execute("INSERT INTO transactions (transaction_id, student_id, action, category, amount, reason_code, timestamp) "
                       "VALUES (?, ?, 'REDEEM', 'REDEMPTION', ?, ?, ?)",
                       (transaction_id, student_id, -item["point_cost"], reward_id, timestamp))
            return transaction_id

    def reverse(self, transaction_id: str, issuer_id: str, timestamp: int) -> str:
        """Undo an award by its issuer. Only awards can be reversed, and only once; the
        balance may not go negative (the student may already have spent the points)."""
        with self._write() as db:
            original = db.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,)).fetchone()
            if original is None or original["action"] != "EARN":
                raise LedgerError("Only an award can be reversed.")
            if original["issuer_id"] != issuer_id:
                raise LedgerError("Only the issuer of an award can reverse it.")
            if db.execute("SELECT 1 FROM transactions WHERE reverses = ?", (transaction_id,)).fetchone():
                raise LedgerError("That award was already reversed.")
            if self._balance(db, original["student_id"]) < original["amount"]:
                raise LedgerError("The student has already spent these points.")
            reversal_id = uuid.uuid4().hex
            db.execute("INSERT INTO transactions (transaction_id, student_id, issuer_id, policy_id, policy_version, action, "
                       "category, amount, reason_code, timestamp, reverses) VALUES (?, ?, ?, ?, ?, 'REVERSE', ?, ?, 'REVERSAL', ?, ?)",
                       (reversal_id, original["student_id"], issuer_id, original["policy_id"], original["policy_version"],
                        original["category"], -original["amount"], timestamp, transaction_id))
            return reversal_id

    def import_dataset(self, dataset: Dataset) -> None:
        """Load a synthetic dataset into an empty ledger in one transaction (demo and tests)."""
        with self._write() as db:
            if db.execute("SELECT 1 FROM students LIMIT 1").fetchone():
                raise LedgerError("The ledger already holds data.")
            for p in dataset.policies.values():
                db.execute("INSERT INTO policies VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (p.policy_id, p.version, p.name, p.category, p.earning_rule,
                            p.intended_objective, p.points_per_award, p.objective_measure))
            db.executemany("INSERT INTO students VALUES (?, ?)", [(s.student_id, s.group) for s in dataset.students])
            for issuer in dataset.issuers:
                db.execute("INSERT INTO issuers VALUES (?, ?)", (issuer.issuer_id, issuer.role))
                db.executemany("INSERT INTO issuer_scope VALUES (?, ?)", [(issuer.issuer_id, p) for p in sorted(issuer.policy_scope)])
            db.executemany("INSERT INTO opportunities VALUES (?, ?, ?, ?)",
                           [(s.student_id, k[0], k[1], c) for s in dataset.students for k, c in s.opportunities.items()])
            db.executemany("INSERT INTO rewards VALUES (?, ?, ?, ?)",
                           [(r.reward_id, r.name, r.point_cost, r.stock) for r in dataset.catalogue])
            db.executemany("INSERT INTO transactions (transaction_id, student_id, issuer_id, policy_id, policy_version, "
                           "action, category, amount, reason_code, timestamp, measure) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [(t.transaction_id, t.student_id, t.issuer_id, t.policy_id, t.policy_version, t.action.value,
                             t.category, t.amount, t.reason_code, t.timestamp, t.measure) for t in dataset.transactions])

    def is_empty(self) -> bool:
        with self._connect() as db:
            return db.execute("SELECT 1 FROM students LIMIT 1").fetchone() is None

    # ---- reads ----

    @staticmethod
    def _balance(db, student_id: str) -> int:
        return db.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE student_id = ?",
                          (student_id,)).fetchone()[0]

    def balance(self, student_id: str) -> int:
        with self._connect() as db:
            return self._balance(db, student_id)

    def balances(self) -> list[dict]:
        with self._connect() as db:
            rows = db.execute("SELECT s.student_id, s.group_label, COALESCE(SUM(t.amount), 0) AS balance "
                              "FROM students s LEFT JOIN transactions t ON t.student_id = s.student_id "
                              "GROUP BY s.student_id ORDER BY s.student_id").fetchall()
        return [dict(r) for r in rows]

    def rewards(self) -> list[dict]:
        with self._connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM rewards ORDER BY point_cost")]

    def load_dataset(self) -> Dataset:
        with self._connect() as db:
            policies = {r["policy_id"]: RewardPolicy(r["policy_id"], r["version"], r["name"], r["category"],
                                                     r["earning_rule"], r["intended_objective"],
                                                     r["points_per_award"], r["objective_measure"])
                        for r in db.execute("SELECT * FROM policies")}
            opps = {}
            for r in db.execute("SELECT * FROM opportunities"):
                opps.setdefault(r["student_id"], {})[(r["policy_id"], r["issuer_id"])] = r["count"]
            students = [StudentContext(r["student_id"], r["group_label"], opps.get(r["student_id"], {}))
                        for r in db.execute("SELECT * FROM students ORDER BY student_id")]
            scopes = {}
            for r in db.execute("SELECT * FROM issuer_scope"):
                scopes.setdefault(r["issuer_id"], set()).add(r["policy_id"])
            issuers = [IssuerContext(r["issuer_id"], r["role"], frozenset(scopes.get(r["issuer_id"], ())))
                       for r in db.execute("SELECT * FROM issuers ORDER BY issuer_id")]
            transactions = [RewardTransaction(r["transaction_id"], r["student_id"], r["issuer_id"], r["policy_id"],
                                              r["policy_version"], Action(r["action"]), r["category"], r["amount"],
                                              r["reason_code"], r["timestamp"], r["measure"])
                            for r in db.execute("SELECT * FROM transactions ORDER BY seq")]
            catalogue = [RewardItem(r["reward_id"], r["name"], r["point_cost"], r["stock"])
                         for r in db.execute("SELECT * FROM rewards")]
        return Dataset(policies, students, issuers, transactions, catalogue)
