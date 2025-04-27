import json
import os

def load_all_configs(config_dir='configs'):
    configs = []
    for filename in os.listdir(config_dir):
        if filename.endswith('.json'):
            path = os.path.join(config_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                configs.append(config)
    return configs
