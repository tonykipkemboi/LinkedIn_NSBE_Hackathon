import argparse
from profile import get_profiles_by_id_or_name
from collections import defaultdict
import profile
import sqlite3
import sys

COL_INDEX_SKILL_NEEDS_ID = 0
COL_INDEX_SKILL_NEEDS_YEAR = 1
COL_INDEX_SKILL_NEEDS_SECTION_INDEX = 2
COL_INDEX_SKILL_NEEDS_SECTION_NAME = 3
COL_INDEX_SKILL_NEEDS_INDUSTRY_NAME = 4
COL_INDEX_SKILL_NEEDS_SKILL_GROUP_CATEGORY = 5
COL_INDEX_SKILL_NEEDS_SKILL_GROUP_NAME = 6
COL_INDEX_SKILL_NEEDS_RANK = 7

COL_INDEX_SKILL_PEN_ID = 0
COL_INDEX_SKILL_PEN_YEAR = 1
COL_INDEX_SKILL_PEN_SKILL_GROUP_CATEGORY = 2
COL_INDEX_SKILL_PEN_SKILL_GROUP_NAME = 3
COL_INDEX_SKILL_PEN_SECTION_INDEX = 4
COL_INDEX_SKILL_PEN_SECTION_NAME = 5
COL_INDEX_SKILL_PEN_INDUSTRY_NAME = 6
COL_INDEX_SKILL_PEN_RATE = 7

def jaccard(list1, list2):
  intersection = len(list(set(list1).intersection(list2)))
  union = (len(list1) + len(list2)) - intersection
  return float(intersection) / union

def calculate_pen_score(pen_rate_dict, industry, skills_list):
  match_any = False
  score = 1
  industry_rates = pen_rate_dict[industry]
  for my_skill in skills_list:
    if my_skill in industry_rates:
      score = score * (industry_rates[my_skill] * 100)
      match_any = True
  if match_any:
    return score
  else:
    return 0.0

parser = argparse.ArgumentParser()
parser.add_argument('--id', '-i', help="The id of the profile", type= int, default= 0)
parser.add_argument('--name', '-n', help="The name of the profile", type= str)
args=parser.parse_args()

if args.id == 0 and args.name is None:
  print('Specify either the --id or the --name of the profile to analyze')
  exit()

db_conn_rank = sqlite3.connect('skillneeds.db')
cursor_rank = db_conn_rank.cursor()
db_conn_pen = sqlite3.connect('skillpen.db')
cursor_pen = db_conn_pen.cursor()

industry_to_needs_list_dict = defaultdict(list)

# Get latest
for row in cursor_rank.execute('select * from skillneeds where year = "2019"'):
  industry_to_needs_list_dict[str(row[COL_INDEX_SKILL_NEEDS_INDUSTRY_NAME])].append(str(row[COL_INDEX_SKILL_NEEDS_SKILL_GROUP_NAME]))

industry_to_skill_pen_list_dict = defaultdict(lambda: defaultdict(int))

for row in cursor_pen.execute('select * from skillpenetration where year = "2019"'):
  industry_to_skill_pen_list_dict[str(row[COL_INDEX_SKILL_PEN_INDUSTRY_NAME])][str(row[COL_INDEX_SKILL_PEN_SKILL_GROUP_NAME])] = row[COL_INDEX_SKILL_PEN_RATE]

db_conn_rank.close()
db_conn_pen.close()

industry_to_total_score_dict = {}

profiles_to_analyze = get_profiles_by_id_or_name(args.id, args.name)

for profile_to_analyze in profiles_to_analyze:
  if profile_to_analyze is None:
    print('This profile does not exist')
    exit()

  #skills_array = ['Computer Networking', 'Software Development Life Cycle (SDLC)', 'Mathematics']

  print("\n\n\n\n")
  print("----------", "Matching skills for profile:", "----------")
  profile_to_analyze.print()
  print("--------------------------------------------------\n")


  for key, value in industry_to_needs_list_dict.items():
    similarity = jaccard(profile_to_analyze.skills, value)
    pen_score = calculate_pen_score(industry_to_skill_pen_list_dict, key, profile_to_analyze.skills) 
    total_score = similarity * pen_score * 100
    if total_score > 0:
      industry_to_total_score_dict[key] = total_score

  for key, value in sorted(industry_to_total_score_dict.items(), key = lambda item: item[1], reverse = True):
    print(' > ', key, "-- Match Score: ", value)
