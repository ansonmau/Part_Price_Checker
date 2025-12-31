from numpy import info
from scripts.misc.Log import MyLogger
from scripts.misc.Utils import ROOT, create_folder, create_file

logger = MyLogger("Init_Module")

dir_settings = ROOT / 'data' / 'settings.json'
dir_memory = ROOT / 'data' / 'item_memory.json'

def init():
    generate_folders()
    generate_files()
    pass 

def generate_folders():
    logger.info("Creating data folder")
    create_folder(ROOT / "data")

def generate_files():
    logger.info("Creating settings file")
    create_file(dir_settings)
    logger.info("Creating memory file")
    create_file(dir_memory)

def init_new_memory():
    import json
    logger.info("Creating new item memory")
    default_memory = {
            "CC": {},
            "AZ": {},
            "NE": {},
            "ME": {},
            }

    with open(dir_memory) as f:
        json.dump(default_memory, f)

