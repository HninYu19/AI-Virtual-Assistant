import sqlite3

conn = sqlite3.connect('baymax.db')
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY, name VARCHAR(255), path VARCHAR(1000))"
cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null, 'OneNote', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE')"
#cursor.execute(query)
#conn.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id INTEGER PRIMARY KEY, name VARCHAR(255), url VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO web_command VALUES (null, 'youtube', 'https://www.youtube.com/')"
cursor.execute(query)
conn.commit()