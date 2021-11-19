import json
import logging
import pandas as pd

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)


logging.info("Fetching heroes data")
f = open("data/heroes/filtered_hero_data.json", "r")
hero_data = json.load(f)
f.close()

logging.info("Fetching roles data")
f = open("data/roles/roles_data.json", "r")
roles_data = json.load(f)
f.close()


hero_roles = []

logging.info("Generating hero vs roles data")
for hero in hero_data:
    for role in hero["roles"]:
        hero_roles.append( (hero["hero_id"], roles_data[role.lower()]) )

logging.info("Creating dataframe and saving as csv")
df = pd.DataFrame(hero_roles, columns=["hero_id", "role_id"])
df.to_csv("data/features/hero_vs_roles.csv", index=False)


logging.info("Done")
