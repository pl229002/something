import sqlite3

connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()

createTable = """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, password TEXT)"""

cursor.execute(createTable)

# Test person has been created --> name: Sobheet, password: test; name: Sobheet2, password: test2