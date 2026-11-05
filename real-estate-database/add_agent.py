
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

# new agent information
new_agent = (
    "Mrs.",
    "Puff",
    "puff.agent@bikinibottom.example",
    "555-0109"
)

try:
    cursor.execute("""
        INSERT INTO Agent (
            first_name, last_name, email, phone
        )
        VALUES (?, ?, ?, ?);
    """, new_agent)

    conn.commit()
    print("New agent added successfully!")

except sqlite3.IntegrityError:
    conn.rollback()
    print("Agent already exists!")

finally:
    conn.close()
