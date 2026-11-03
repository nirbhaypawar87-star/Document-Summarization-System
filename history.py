
import sqlite3
from datetime import datetime

DB_NAME = "summary_history.db"


def create_table():
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                original_words INTEGER,
                summary_words INTEGER,
                summary_text TEXT,
                created_at TEXT
            )
        """)


def save_summary(filename, original_words, summary_words, summary_text):
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            INSERT INTO summaries
            (filename, original_words, summary_words, summary_text, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            filename,
            original_words,
            summary_words,
            summary_text,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))


def get_history():
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.execute("""
            SELECT id, filename, original_words, summary_words,
                   summary_text, created_at
            FROM summaries
            ORDER BY id DESC
        """)
        return cursor.fetchall()



def delete_summary(summary_id):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.execute(
        "DELETE FROM summaries WHERE id = ?",
        (summary_id,)
    )

    connection.commit()
    connection.close()

