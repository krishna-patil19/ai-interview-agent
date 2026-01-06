import sqlite3
import os

DB_PATH = os.path.join("data", "sales_agent.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT,
        personality TEXT,
        resource TEXT,
        conversation TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        session_id TEXT,
        report TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_session(session_id, personality, resource, conversation):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO sessions VALUES (?, ?, ?, ?)",
        (session_id, personality, resource, conversation)
    )

    conn.commit()
    conn.close()

def save_evaluation(session_id, report):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO evaluations VALUES (?, ?)",
        (session_id, report)
    )

    conn.commit()
    conn.close()
