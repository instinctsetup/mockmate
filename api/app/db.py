"""Storage: Postgres when DATABASE_URL is reachable, else in-memory.

The app stays fully functional for demos without Postgres; docker-compose
wires the real thing. Same for Redis (cache.py).
"""
import os

_pool = None
_mem: dict = {}


def using_postgres() -> bool:
    return _conn() is not None


def _conn():
    global _pool
    if _pool is False:
        return None
    if _pool is not None:
        return _pool
    url = os.environ.get("DATABASE_URL")
    if not url:
        _pool = False
        return None
    try:
        import psycopg2
        _pool = psycopg2.connect(url)
        _pool.autocommit = True
        _init_schema(_pool)
        return _pool
    except Exception:
        _pool = False
        return None


def _init_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id SERIAL PRIMARY KEY,
            company TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT now(),
            notes TEXT DEFAULT ''
        )""")


def save_session(company: str, notes: str = "") -> int:
    conn = _conn()
    if conn is None:
        sid = len(_mem) + 1
        _mem[sid] = {"company": company, "notes": notes}
        return sid
    with conn.cursor() as cur:
        cur.execute("INSERT INTO sessions (company, notes) VALUES (%s, %s) RETURNING id",
                    (company, notes))
        return cur.fetchone()[0]


def list_sessions() -> list[dict]:
    conn = _conn()
    if conn is None:
        return [{"id": k, **v} for k, v in _mem.items()]
    with conn.cursor() as cur:
        cur.execute("SELECT id, company, notes, created_at FROM sessions ORDER BY id DESC LIMIT 50")
        return [{"id": r[0], "company": r[1], "notes": r[2], "created_at": str(r[3])} for r in cur.fetchall()]
