import sqlite3
from datetime import datetime


DB = "ixxy_codes.db"


def connect():
    return sqlite3.connect(DB)


def init_db():
    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        last_reward TEXT DEFAULT ''
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS codes(
        code TEXT PRIMARY KEY,
        reward INTEGER,
        used INTEGER DEFAULT 0,
        user_id INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)

    db.commit()
    db.close()


def add_user(user_id, username):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, username)
        VALUES (?,?)
        """,
        (user_id, username)
    )

    db.commit()
    db.close()


def get_last_reward(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT last_reward FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cur.fetchone()

    db.close()

    return result[0] if result else ""


def set_last_reward(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE users
        SET last_reward=?
        WHERE user_id=?
        """,
        (datetime.now().strftime("%Y-%m-%d"), user_id)
    )

    db.commit()
    db.close()