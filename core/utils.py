import os
import json
import time
import requests
from datetime import datetime

def get_proxy(config):
    if config.get('enabled', False):
        proxy = config.get('proxy', '')
        username = config.get('username', '')
        password = config.get('password', '')
        if username and password:
            proxy = proxy.replace('://', f'://{username}:{password}@')
        return {'http': proxy, 'https': proxy}
    return None

def save_log(content, name, output_dir="logs"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{name}_{timestamp}.txt"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
    return filename

def load_config(config_file="config.json"):
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_config(config, config_file="config.json"):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=2).text
    except:
        try:
            return requests.get('http://ip-api.com/json', timeout=2).json().get('query', 'Unknown')
        except:
            return "Unknown"
