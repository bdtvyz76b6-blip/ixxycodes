import sqlite3
import random
import string

from datetime import datetime, timedelta


DB = "users.db"


def connect():
    return sqlite3.connect(DB)



# =====================
# СОЗДАНИЕ БАЗЫ
# =====================

def init_db():

    conn = connect()
    cur = conn.cursor()


    # USERS (ixxy VPN)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        user_id INTEGER PRIMARY KEY,

        username TEXT,

        first_name TEXT,

        subscription TEXT DEFAULT 'none',

        subscription_until TEXT DEFAULT '',

        subscription_link TEXT DEFAULT '',

        uuid TEXT DEFAULT '',

        trial_used INTEGER DEFAULT 0,

        pending_days INTEGER DEFAULT 0,

        notify INTEGER DEFAULT 1,

        accepted_terms INTEGER DEFAULT 0,

        created_at TEXT DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # КОДЫ

    cur.execute("""
    CREATE TABLE IF NOT EXISTS codes(

        code TEXT PRIMARY KEY,

        reward INTEGER,

        used INTEGER DEFAULT 0,

        user_id INTEGER,

        created_at TEXT

    )
    """)



    # УДАЧА

    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_rewards(

        user_id INTEGER PRIMARY KEY,

        last_reward TEXT

    )
    """)



    conn.commit()
    conn.close()





# =====================
# USERS
# =====================

def add_user(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    INSERT OR IGNORE INTO users(user_id)

    VALUES(?)

    """,
    (user_id,))


    conn.commit()
    conn.close()





# =====================
# ГЕНЕРАЦИЯ КОДА
# =====================

def generate_code():

    chars = string.ascii_uppercase + string.digits


    return "IXXY-" + "".join(
        random.choice(chars)
        for _ in range(8)
    )





def create_code(user_id, days):

    conn = connect()
    cur = conn.cursor()


    code = generate_code()


    cur.execute("""
    INSERT INTO codes
    (
        code,
        reward,
        user_id,
        created_at
    )

    VALUES(?,?,?,?)

    """,
    (
        code,
        days,
        user_id,
        datetime.now().strftime("%Y-%m-%d")
    ))


    conn.commit()
    conn.close()


    return code





# =====================
# МОИ КОДЫ
# =====================

def get_codes(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT code,reward,used

    FROM codes

    WHERE user_id=?

    """,
    (user_id,))


    data = cur.fetchall()


    conn.close()


    return data





# =====================
# АКТИВАЦИЯ КОДА
# =====================

def activate_code(code):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT reward,used

    FROM codes

    WHERE code=?

    """,
    (code,))


    result = cur.fetchone()


    if not result:

        conn.close()
        return None



    reward, used = result



    if used == 1:

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
# ДОБАВИТЬ ДНИ VPN
# =====================

def add_days(user_id, days):

    add_user(user_id)


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


    return new_date





# =====================
# УДАЧА ДНЯ
# =====================

def daily_available(user_id):

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


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    if not result:

        return True


    return result[0] != today





def save_daily(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    INSERT OR REPLACE INTO daily_rewards

    VALUES(?,?)

    """,
    (
        user_id,
        datetime.now().strftime("%Y-%m-%d")
    ))


    conn.commit()
    conn.close()
    
    
    
    # =====================
# СОВМЕСТИМОСТЬ СО СТАРЫМ REWARDS.PY
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
# СОВМЕСТИМОСТЬ LUCK.PY
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


    today = datetime.now().strftime("%Y-%m-%d")


    # первый раз можно
    if not result:
        return True


    # если сегодня уже забрал — нельзя
    if result[0] == today:
        return False


    return True