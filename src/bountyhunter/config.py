import os
import json
from dotenv import load_dotenv


load_dotenv()


def initial_config(config_path):
    config_dict = {
        "prefix": os.environ.get("PREFIX") or "$",
        "token": os.environ.get("TOKEN"),
        "permissions": int(os.environ.get("PERMISSIONS")) or 8,
        "application_id": int(os.environ.get("APPLICATION_ID")) or 0,
        "sync_commands_globally": os.environ.get("SYNC_COMMANDS_GLOBALLY") is not None,
        "owners": os.environ.get("OWNERS").split(",")
    }
    owners = []
    for o in config_dict['owners']:
        owners.append(int(0))

    config_dict['owners'] = owners
    with open(config_path, 'w') as file:
        file.write(json.dumps(config_dict))

