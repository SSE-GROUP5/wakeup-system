# config.py

import json


def load_json(name):
    try:
        with open(name, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print(f"Error: Couldn't properly read file '{name}'. "
              "Either the file is missing or it contains invalid JSON.")
        if name == 'config.json':
            default_config = {
                "user_made_sounds": {
                    "trigger_words": {},
                    "sound_pattern": {}
                }
            }
            save_json(default_config, 'config.json')
            return default_config
        else:
            raise FileNotFoundError(f"No such file or directory: '{name}'")


def save_json(config, name):
    with open(name, 'w') as f:
        json.dump(config, f, indent=2)


def update_user_made_sounds(key, sub_key, value):
    config = load_json('config.json')
    config['user_made_sounds'][key][sub_key] = value
    save_json(config, 'config.json')


def clear_user_made_sounds():
    config = load_json('config.json')

    config[str('user_made_sounds')] = {
        "trigger_words": {},
        "sound_pattern": {}
    }
    save_json(config, 'config.json')
