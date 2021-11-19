import json
import requests
import logging


logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

def process_hero(res):
    return {k: res[k] for k in required_keys}


required_keys = [
'id', 'name', 'localized_name', 'primary_attr', 'attack_type', 'roles', 
'base_health', 'base_health_regen', 'base_mana', 'base_mana_regen', 'base_armor', 'base_mr', 
'base_attack_min', 'base_attack_max', 'base_str', 'base_agi', 'base_int', 'str_gain', 
'agi_gain', 'int_gain', 'attack_range', 'projectile_speed', 'attack_rate', 'move_speed', 
'legs', 'hero_id'
]


hero_stats_url = "https://api.opendota.com/api/heroStats"

logging.info("Sending get request")
response = requests.get(hero_stats_url)

hero_data = response.json()
filtered_data = []

logging.info("Processing data")
for hero in hero_data:
    filtered_data.append(process_hero(hero))

logging.info("Writing to file")
with open("data/heroes/filtered_hero_data.json", "w") as f:
    json.dump(filtered_data, f, indent=4)
    f.close()

logging.info("Done")

