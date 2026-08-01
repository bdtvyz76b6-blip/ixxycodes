import sqlite3
from datetime import datetime, timedelta
import random
import string

DB = "users.db"


def connect():
    return sqlite3.connect(DB)



# =====================
# КОДЫ
# =====================

def create_codes_table():

    db = connect()
    cur = db.cursor()

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



def create_code(code, reward):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO codes
    VALUES (?,?,?,?,?)
    """,
    (
        code,
        reward,
        0,
        0,
        datetime.now().isoformat()
    ))

    db.commit()
    db.close()



def bind_code(code,user_id):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    UPDATE codes
    SET user_id=?
    WHERE code=?
    """,
    (
        user_id,
        code
    ))

    db.commit()
    db.close()



def get_codes(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    SELECT code,used
    FROM codes
    WHERE user_id=?
    """,
    (user_id,))

    data = cur.fetchall()

    db.close()

    return data



def activate_code(code,user_id):

    db = connect()
    cur = db.cursor()


    cur.execute("""
    SELECT reward,used
    FROM codes
    WHERE code=?
    """,
    (code,))


    result = cur.fetchone()


    if not result:
        db.close()
        return None


    reward,used=result


    if used:
        db.close()
        return "used"



    cur.execute("""
    UPDATE codes
    SET used=1,
        user_id=?
    WHERE code=?
    """,
    (
        user_id,
        code
    ))


    db.commit()
    db.close()


    return reward



# =====================
# VPN ПОДПИСКА
# =====================


def add_days(user_id,days):

    db = connect()
    cur = db.cursor()


    cur.execute("""
    SELECT subscription_until
    FROM users
    WHERE user_id=?
    """,
    (user_id,))


    result=cur.fetchone()


    now=datetime.now()


    if result and result[0]:

        try:
            current=datetime.fromisoformat(
                result[0]
            )

        except:
            current=now

    else:
        current=now



    if current < now:
        current=now



    new_date=current+timedelta(days=days)



    cur.execute("""
    UPDATE users
    SET subscription_until=?
    WHERE user_id=?
    """,
    (
        new_date.isoformat(),
        user_id
    ))


    db.commit()
    db.close()



def user_exists(user_id):

    db=connect()
    cur=db.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE user_id=?",
        (user_id,)
    )

    result=cur.fetchone()

    db.close()

    return result is not None