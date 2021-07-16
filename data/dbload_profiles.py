import random
import sqlite3

def load():
  db_conn = sqlite3.connect('profiles.db')
  cursor = db_conn.cursor()

  cursor.execute("drop table if exists profiles")
  cursor.execute("create table profiles (id integer PRIMARY KEY, name text not null, skillset text not null, connection_weight integer not null)")

  names_for_profiles = []
  all_skills = []

  with open('list_of_names.txt', newline='') as f:
    names_for_profiles = f.read().splitlines()

  with open('list_of_skills.txt', newline='') as f:
    all_skills = f.read().splitlines()

  id = 1
  for name in names_for_profiles:
    skill_sample = random.sample(all_skills, 4)
    connection_weight = random.randint(0,10)
    profile_skills = ','.join(skill_sample)
    data_tuple = (id, name, profile_skills, connection_weight)
    cursor.execute("insert into profiles values (?, ?, ?, ?);", data_tuple)
    id = id + 1
    db_conn.commit()

  db_conn.close()