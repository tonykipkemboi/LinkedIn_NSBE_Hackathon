import csv
import sqlite3

db_conn = sqlite3.connect('skillneeds.db')
cursor = db_conn.cursor()

cursor.execute("create table skillneeds (id integer PRIMARY KEY, year integer not null, isic_section_index text not null, isic_section_name text not null, industry_name text not null, skill_group_category text not null, skill_group_name text not null, rank integer not null)")

id = 1

with open('public_use-industry-skills-needs.csv', newline='') as csvfile:
  skillreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in skillreader:
    if row[0] == "":
      continue
    row.insert(0, id)
    cursor.execute("insert into skillneeds values (?, ?, ?, ?, ?, ?, ?, ?)", row)
    id = id + 1
    db_conn.commit()

db_conn.close()
