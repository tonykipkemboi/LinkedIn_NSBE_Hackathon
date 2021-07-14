import sqlite3

db_conn = sqlite3.connect('skillneeds.db')
cursor = db_conn.cursor()

for row in cursor.execute('select count(*) from skillneeds'):
  print(row)

db_conn.close()

