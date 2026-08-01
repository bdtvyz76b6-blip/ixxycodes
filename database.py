import sqlite3
from datetime import datetime, timedelta


DB = "users.db"


def connect():
    return sqlite3.connect(DB)



def init_db():

    db = connect()
    cur = db.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS codes(
        code TEXT PRIMARY KEY,
        reward INTEGER,
        used INTEGER DEFAULT 0,
        user_id INTEGER,
        created_at TEXT
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_rewards(
        user_id INTEGER PRIMARY KEY,
        last_reward TEXT
    )
    """)


    db.commit()
    db.close()



# =====================
# КОДЫ
# =====================


def save_code(code, reward, user_id):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO codes
    VALUES(?,?,?,?,?)
    """,
    (
        code,
        reward,
        0,
        user_id,
        datetime.now().isoformat()
    ))

    db.commit()
    db.close()



def get_codes(user_id):

    db = connect()
    cur = db.cursor()

    cur.execute("""
    SELECT code, reward, used
    FROM codes
    WHERE user_id=?
    """,
    (user_id,))


    data = cur.fetchall()

    db.close()

    return data



def activate_code(code):

    db = connect()
    cur = db.cursor()


    cur.execute("""
    SELECT reward, used
    FROM codes
    WHERE code=?
    """,
    (code,))


    result = cur.fetchone()


    if not result:
        db.close()
        return None


    reward, used = result


    if used:
        db.close()
        return "used"


    cur.execute("""
    UPDATE codes
    SET used=1
    WHERE code=?
    """,
    (code,))


    db.commit()
    db.close()


    return reward



# =====================
# VPN ПРОДЛЕНИЕ
# =====================


def add_days(user_id, days):

    db = connect()
    cur = db.cursor()


    cur.execute("""
    SELECT subscription_until
    FROM users
    WHERE user_id=?
    """,
    (user_id,))


    result = cur.fetchone()


    now=datetime.now()


    if result and result[0]:

        try:
            date=datetime.fromisoformat(result[0])

        except:
            date=now

    else:
        date=now



    if date < now:
        date=now



    new=date+timedelta(days=days)


    cur.execute("""
    UPDATE users
    SET subscription_until=?
    WHERE user_id=?
    """,
    (
        new.isoformat(),
        user_id
    ))


    db.commit()
    db.close()



# =====================
# УДАЧА
# =====================


def can_daily(user_id):

    db=connect()
    cur=db.cursor()


    cur.execute(
    """
    SELECT last_reward
    FROM daily_rewards
    WHERE user_id=?
    """,
    (user_id,))


    result=cur.fetchone()

    db.close()


    if not result:
        return True


    return result[0] != datetime.now().strftime("%Y-%m-%d")



def save_daily(user_id):

    db=connect()
    cur=db.cursor()


    cur.execute("""
    INSERT OR REPLACE INTO daily_rewards
    VALUES(?,?)
    """,
    (
        user_id,
        datetime.now().strftime("%Y-%m-%d")
    ))


    db.commit()
    db.close()