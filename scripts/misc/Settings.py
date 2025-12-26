import json
from scripts.misc import Utils
from scripts.misc.Utils import ROOT

SETTINGS_DIR = ROOT / "data" / "settings.json"

def check_settings_file_exists():
    return SETTINGS_DIR.exists()

class Settings():
    default_settings = {
        "lookup": {
            "AZ": True,
            "PCP": True,
            "CC": True,
            "NE": True,
            "ME": True
        }
    }

    def __init__(self):
        self.settings = self.default_settings

        if not check_settings_file_exists():
            Utils.create_folder(ROOT / "data")
            Utils.create_file(ROOT / "data" / "settings.json")
            self.save()

    def load_from_file(self):
        with open(ROOT / "data" / "settings.json", 'r') as f:
            self.settings = json.load(f)
    
    def save(self):
        with open(ROOT / "data" / "settings.json", 'w') as f:
            json.dump(self.settings, f)
        



