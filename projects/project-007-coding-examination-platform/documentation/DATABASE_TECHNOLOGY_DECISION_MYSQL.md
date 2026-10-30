# Database Technology Decision — MySQL

## Decision
The full P001 operational platform uses **MySQL Server** as its canonical relational database. **MySQL Workbench** is the local graphical administration, SQL and modelling client used by the developer. SQLite remains permitted only for isolated legacy/research fixtures and fast unit tests where database-specific behavior is not under test.

## Why MySQL
P001 is now a multi-user examination platform with strongly related operational data: users/roles, examinations/questions, candidate assignments, sessions, submissions, evidence, verification and audit records. MySQL provides a client-server relational DBMS, transactions, foreign-key integrity, indexes, concurrent connections and a database that can be inspected and administered independently through Workbench.

## Alternatives considered
- **SQLite:** excellent for the original bounded research prototype and deterministic tests; less representative of the intended multi-user deployed system because it is an embedded file database.
- **PostgreSQL:** technically suitable, but would add a second database toolchain when the developer has selected MySQL/Workbench; no current requirement justifies that switch.
- **NoSQL/document database:** rejected as the primary store because the core model is relational and depends heavily on referential integrity and auditable relationships.

## Consequences
1. The operational persistence layer must not embed SQLite-only SQL.
2. Database connection/configuration must be environment-based; credentials must not be committed.
3. Schema evolution will use versioned SQL migrations.
4. Integration tests must exercise MySQL-specific behavior before deployment claims.
5. The ERD and physical schema must stay synchronized.
6. MySQL Workbench is not the database itself; it connects to MySQL Server.
7. The research mechanism remains logically isolated from operational product tables.

## Target connection
```text
Browser -> FastAPI -> repository/data-access layer -> MySQL Server
                                                ^
                                                |
                                      MySQL Workbench
                                      administration/design
```

## Migration boundary
FD-01 was first implemented against the existing SQLite abstraction. Full-product development now introduces a MySQL-capable persistence path before FD-02 examination management. Existing research data/schema will not be destructively rewritten merely to make the product layer use MySQL.
