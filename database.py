import sqlite3

DB_NAME = "chatbot.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def create_db():
    conn = get_conn()
    cur = conn.cursor()
    with open("create_table.sql", "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()
    
def insert_db():
    conn = get_conn()
    cur = conn.cursor()
    with open("insert_to_table.sql", "r") as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()

def save_conversation(message, reply):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conversations (message, reply) VALUES (?, ?)",
        (message, reply)
    )
    conn.commit()
    conn.close()

def get_orders(order_id: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT status FROM orders WHERE order_id=?", (order_id,))
    res = cur.fetchone()
    conn.close()
    return res[0] if res else None

def get_products():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT product_name, product_description FROM products")
    res = cur.fetchall()
    conn.close()
    return res

def get_faqs():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT question, answer FROM faqs")
    res = cur.fetchall()
    conn.close()
    return res