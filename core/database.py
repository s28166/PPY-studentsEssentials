import sqlite3

conn = sqlite3.connect('../db/database.db', check_same_thread=False)
cursor = conn.cursor()