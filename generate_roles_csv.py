import json
import logging
import pandas as pd

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)


logging.info("Fetching roles data")
f = open("data/roles/roles_data.json", "r")
roles_data: dict = json.load(f)
f.close()


logging.info("Generating roles dataframe")
role_names = list(roles_data.keys())
roles_df = pd.DataFrame({"role": role_names})

logging.info("Generating roles csv")
roles_df.to_csv('data/features/roles_data.csv', index=False)


logging.info("Done")