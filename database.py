import sqlite3
from datetime import datetime, timedelta


DB = "users.db"


def connect():
    return sqlite3.connect(DB)



# =====================
# ДОБАВЛЯЕМ ТАБЛИЦЫ IXYY CODES
# =====================

def init_codes():

    conn = connect()
    cur = conn.cursor()


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


    conn.commit()
    conn.close()



# =====================
# СОЗДАНИЕ КОДА
# =====================

def save_code(code, reward, user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    INSERT INTO codes
    (
        code,
        reward,
        user_id,
        created_at
    )

    VALUES (?,?,?,?)

    """,
    (
        code,
        reward,
        user_id,
        datetime.now().strftime("%Y-%m-%d")
    ))


    conn.commit()
    conn.close()



# =====================
# МОИ КОДЫ
# =====================

def get_codes(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT code, reward, used
    FROM codes
    WHERE user_id=?

    """,
    (user_id,))


    result = cur.fetchall()


    conn.close()

    return result



# =====================
# АКТИВАЦИЯ КОДА
# =====================

def activate_code(code):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT reward, used
    FROM codes
    WHERE code=?

    """,
    (code,))


    result = cur.fetchone()


    if not result:

        conn.close()
        return None


    reward, used = result


    if used:

        conn.close()
        return "used"



    cur.execute("""
    UPDATE codes

    SET used=1

    WHERE code=?

    """,
    (code,))


    conn.commit()
    conn.close()


    return reward



# =====================
# ДОБАВЛЕНИЕ ДНЕЙ VPN
# =====================

def add_days(user_id, days):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT subscription_until

    FROM users

    WHERE user_id=?

    """,
    (user_id,))


    result = cur.fetchone()


    now = datetime.now()


    if result and result[0]:

        try:

            old = datetime.strptime(
                result[0],
                "%Y-%m-%d"
            )

        except:

            old = now

    else:

        old = now



    if old < now:

        old = now



    new_date = (
        old +
        timedelta(days=days)
    ).strftime(
        "%Y-%m-%d"
    )



    cur.execute("""
    UPDATE users

    SET

    subscription='vip',

    subscription_until=?

    WHERE user_id=?

    """,
    (
        new_date,
        user_id
    ))


    conn.commit()
    conn.close()



# =====================
# УДАЧА ДНЯ
# =====================

def can_daily(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT last_reward

    FROM daily_rewards

    WHERE user_id=?

    """,
    (user_id,))


    result = cur.fetchone()


    conn.close()


    today=datetime.now().strftime(
        "%Y-%m-%d"
    )


    if not result:

        return True


    return result[0] != today



def save_daily(user_id):

    conn=connect()
    cur=conn.cursor()


    cur.execute("""
    INSERT OR REPLACE INTO daily_rewards

    VALUES (?,?)

    """,
    (
        user_id,
        datetime.now().strftime("%Y-%m-%d")
    ))


    conn.commit()
    conn.close()