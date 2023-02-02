import os
import json
from dotenv import load_dotenv


load_dotenv()


def initial_config(config_path: str, filename="default_config.json"):
    """
    :param config_path: Path of the directory you want to store config in
    :param filename: Filename (no path) of the json file you want to store the config in.

    :return config_dict: dictionary of config values
    """
    config_dict = {
        "config_path": os.path.join(config_path, filename),
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
    with open(config_dict['config_path'], 'w') as file:
        file.write(json.dumps(config_dict))

    return config_dict