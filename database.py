import sqlite3
import json
import os

DB_PATH = os.getenv("DB_PATH", "face_auth.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            email     TEXT UNIQUE NOT NULL,
            embedding TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_user(name, email, embedding):

    embedding_json = json.dumps(list(embedding))

    conn = get_connection()
    conn.execute(
        "INSERT INTO users (name, email, embedding) VALUES (?, ?, ?)",
        (name, email, embedding_json)
    )
    conn.commit()
    conn.close()


def get_user_embedding(email):
  
    conn = get_connection()
    row = conn.execute(
        "SELECT email, embedding FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()

    if row is None:
        return None

    email_val, embedding_json = row
    return email_val, json.loads(embedding_json)