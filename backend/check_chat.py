import sqlite3

conn = sqlite3.connect("legalbot.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(chat_history);")

columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()