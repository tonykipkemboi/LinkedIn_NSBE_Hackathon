import csv
import sqlite3

def load():
  db_conn = sqlite3.connect('skillpen.db')
  cursor = db_conn.cursor()

  cursor.execute("drop table if exists skillpenetration")
  cursor.execute("create table skillpenetration (id integer PRIMARY KEY, year integer not null, skill_group_category text not null, skill_group_name text not null, isic_section_index text not null, isic_section_name text not null, industry_name text not null, penetration_rate float not null)")

  id = 1

  with open('public_use-skill-penetration.csv', newline='') as csvfile:
    skillpen = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in skillpen:
      if row[0] == "":
        continue
      row.insert(0, id)
      cursor.execute("insert into skillpenetration values (?, ?, ?, ?, ?, ?, ?, ?)", row)
      id = id + 1
      db_conn.commit()

  db_conn.close()