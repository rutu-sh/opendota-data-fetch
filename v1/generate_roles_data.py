import json
import logging

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)


roles = ["carry", "nuker", "initiator", "disabler", "durable", "escape", "support", "pusher", "jungler"]
role_ids = [i for i in range(len(roles))]

logging.info("Generating roles dict")
role_data = dict(zip(roles, role_ids))

logging.info("Saving roles dict as a json file")
with open("data/roles/roles_data.json", "w") as f: 
    json.dump(role_data, f, indent=4)
    f.close()

logging.info("Done")

