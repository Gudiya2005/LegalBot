import sqlite3

conn = sqlite3.connect("legalbot.db")

cursor = conn.cursor()

cursor.execute("""
SELECT id, user_id, role, message
FROM chat_history
ORDER BY id;
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()