#PLACEHOLDER FILE UNTIL WE HAVE MONGODB UP

import sqlite3

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
    DROP TABLE IF EXISTS profiles;
    CREATE TABLE profiles (
        username TEXT PRIMARY KEY,
        password TEXT
    );
""")

db.commit()
db.close()
