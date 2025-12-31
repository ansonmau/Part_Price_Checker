from scripts.misc.Log import MyLogger
from scripts.misc.Utils import ROOT, create_folder, create_file

logger = MyLogger("Init_Module")

def init():
    generate_folders()
    generate_files()
    pass 

def generate_folders():
    logger.debug("Creating data folder")
    create_folder(ROOT / "data")

def generate_files():
    logger.debug("Creating settings file")
    create_file(ROOT / "data" / "settings.json")
    create_file(ROOT / "data" / "item_memory.json")
