from pathlib import Path
import json

LOG_FILE = "./doc/log.json"

def load_json(key):
    with open(LOG_FILE, "r", encoding="utf8") as json_file:
        log = json.load(json_file)
    
    return log[key]

class Config():
    LOG_FILE = "./doc/log.json"
    DB = Path(Path.cwd().parent, "db.db")

    BAHA_IMG_FREQUENCY = 12
