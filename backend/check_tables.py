import sqlite3

conn = sqlite3.connect("legalbot.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT name FRO sqlite_master WHERE type='tabel';"
)

tables = cursor.fetchall()

print("Tables:")

for table in tables:
    print("-", table[0])

conn.close()