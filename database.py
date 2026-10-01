import sqlite3
from datetime import datetime
from typing import List, Dict


class ChatDatabase:
    """Small SQLite database layer for chat history and mood tracking."""

    def __init__(self, database_name: str = "mental_health.db"):
        self.database_name = database_name
        self.create_tables()

    def connect(self):
        connection = sqlite3.connect(self.database_name)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                mood TEXT NOT NULL,
                crisis_detected INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mood_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                mood TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()
        connection.close()

    def save_chat(
        self,
        user_id: str,
        user_message: str,
        bot_response: str,
        mood: str,
        crisis_detected: bool,
    ):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO chat_history
            (user_id, user_message, bot_response, mood,
             crisis_detected, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                user_message,
                bot_response,
                mood,
                int(crisis_detected),
                datetime.utcnow().isoformat(),
            ),
        )

        connection.commit()
        connection.close()

    def save_mood(self, user_id: str, mood: str):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO mood_history
            (user_id, mood, created_at)
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                mood,
                datetime.utcnow().isoformat(),
            ),
        )

        connection.commit()
        connection.close()

    def get_history(
        self,
        user_id: str,
        limit: int = 20,
    ) -> List[Dict]:
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, user_id, user_message,
                   bot_response, mood,
                   crisis_detected, created_at
            FROM chat_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        )

        rows = cursor.fetchall()
        connection.close()

        return [dict(row) for row in rows]

    def get_moods(
        self,
        user_id: str,
        limit: int = 30,
    ) -> List[Dict]:
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, user_id, mood, created_at
            FROM mood_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        )

        rows = cursor.fetchall()
        connection.close()

        return [dict(row) for row in rows]

    def delete_history(self, user_id: str):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM chat_history WHERE user_id = ?",
            (user_id,),
        )

        cursor.execute(
            "DELETE FROM mood_history WHERE user_id = ?",
            (user_id,),
        )

        connection.commit()
        connection.close()


if __name__ == "__main__":
    database = ChatDatabase()
    print("Database initialized successfully.")
