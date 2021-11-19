import json
import logging
import pandas as pd


logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)


val_cols = [
    'hero_idx', 'hero_id', 'base_health_regen', 'base_mana_regen', 
    'base_armor', 'base_attack_min', 'base_attack_max', 'base_str', 'base_agi', 
    'base_int', 'str_gain', 'agi_gain', 'int_gain', 'attack_range', 'projectile_speed', 
    'attack_rate', 'move_speed', 'legs'
    ]

def process_hero(hero):    
    hero_vals = {k: hero[k] for k in val_cols}
    hero_vals['attack_type'] = 1 if hero['attack_type'].lower() == "melee" else 0
    return hero_vals

logging.info("Fetching hero data")
f = open("data/heroes/filtered_hero_data.json")
hero_data = json.load(f)
f.close()
logging.info(f"Fetched data for {len(hero_data)} heroes")

logging.info("Processing heroes")
hero_vals = [process_hero(hero) for hero in hero_data]


logging.info("Writing to processed_heros.json")
with open("data/heroes/processed_hero.json", "w") as f:
    json.dump(hero_vals, f,  indent=4)
    f.close()

logging.info("Generating processed_hero.csv")
df = pd.DataFrame(hero_vals, columns=val_cols)
df = df[val_cols]
df.to_csv("data/features/processed_hero.csv", index=False)

logging.info("Done")