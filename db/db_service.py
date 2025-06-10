import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = "postgresql://postgres:[g?Rskk@r*ZTF6r3]@db.nunviuaahirisqmlzryb.supabase.co:5432/postgres"

USER = "postgres.nunviuaahirisqmlzryb"
PASSWORD = "g?Rskk@r*ZTF6r3"
HOST = "aws-0-eu-west-3.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"

def get_connection():
     return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

# USERS

def insert_user(user):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (id, username)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (user["id"], user["username"]))
            conn.commit()

def get_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            return cur.fetchall()
        
def get_user_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()

def check_if_user_exists(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s LIMIT 1", (user_id,))
            return cur.fetchone() is not None

def update_user(user):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users SET username = %s WHERE id = %s
            """, (user["username"], user["id"]))
            conn.commit()

def delete_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()

# CARDS

def insert_card(card):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cards (code, version, name, url, image)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (card["code"], card["version"], card["name"], card["url"], card["image"]))
            return cur.fetchone()[0]

def get_all_cards():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM cards")
            return cur.fetchall()

def update_card(card):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE cards SET code=%s, version=%s, name=%s, url=%s, image=%s WHERE id=%s
            """, (card["code"], card["version"], card["name"], card["url"], card["image"], card["id"]))
            conn.commit()

def delete_card(card_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cards WHERE id = %s", (card_id,))
            conn.commit()

# TRACKED_CARDS

def insert_tracked_card(tc):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tracked_cards (user_id, card_id, country, condition, quantity, last_price, last_check)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id, card_id) DO NOTHING
                RETURNING id
            """, (tc["user_id"], tc["card_id"], tc["country"], tc["condition"], tc["quantity"], tc["last_price"], tc["last_check"]))
            return cur.fetchone()[0] if cur.rowcount > 0 else None

def get_all_tracked_cards():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tracked_cards")
            return cur.fetchall()

def update_tracked_card(tc):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE tracked_cards
                SET country=%s, condition=%s, quantity=%s, last_price=%s, last_check=%s
                WHERE user_id=%s AND card_id=%s
            """, (tc["country"], tc["condition"], tc["quantity"], tc["last_price"], tc["last_check"], tc["user_id"], tc["card_id"]))
            conn.commit()

def delete_tracked_card(tracked_card_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tracked_cards WHERE id = %s", (tracked_card_id,))
            conn.commit()

# PRICE_HISTORY

def insert_price_history(ph):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO price_history (tracked_card_id, price, checked_at)
                VALUES (%s, %s, %s)
            """, (ph["tracked_card_id"], ph["price"], ph["checked_at"]))
            conn.commit()

def get_all_price_history():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM price_history")
            return cur.fetchall()

def delete_price_history_for_card(tracked_card_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM price_history WHERE tracked_card_id = %s", (tracked_card_id,))
            conn.commit()
