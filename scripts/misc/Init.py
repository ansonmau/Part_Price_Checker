from numpy import info
from scripts.misc.Log import MyLogger
from scripts.misc.Utils import ROOT, create_folder, create_file
import json

logger = MyLogger("Init_Module")

# ╭────────────────────────────────────────────────╮
# │                  Directories                   │
# ╰────────────────────────────────────────────────╯
dir_logs     = ROOT / 'logs'
dir_data     = ROOT / 'data'
dir_settings = dir_data / 'settings.json'
dir_memory   = dir_data / 'item_memory.json'

# ╭────────────────────────────────────────────────╮
# │                      api                       │
# ╰────────────────────────────────────────────────╯
# ── inits everything ──────────────────────────────────────────────────
def init():
    _init_dir(dir_data     , 'data folder' , folder=True)
    _init_dir(dir_logs     , 'logs folder' , folder=True)
    _init_dir(dir_settings , 'settings file')
    _init_dir(dir_memory   , 'memory file')

    if not _check_memory():
        init_new_memory()

# ── just in case memory needs to be created itself ────────────────────
def init_new_memory():
    logger.info("Creating new item memory")
    default_memory = _get_default_memory()

    with open(dir_memory, 'w') as f:
        json.dump(default_memory, f, indent=4)

# ╭────────────────────────────────────────────────╮
# │                    helpers                     │
# ╰────────────────────────────────────────────────╯
# ── create file / folder ──────────────────────────────────────────────
def _init_dir(dir, name, folder=False):
    logger.begin_msg(f"Checking for {name}")
    if dir.exists():
        logger.end_msg("OK")
    else:
        logger.end_msg("FAIL")
        logger.begin_msg(f'Creating {name}')
        if folder:
            create_folder(dir)
        else:
            create_file(dir)
        logger.end_msg('OK')

# ── checks if memory file exists and is valid ─────────────────────────
def _check_memory():
    # exists?
    if not dir_memory.exists():
        return False

    # is valid? 
    # checks keys against default template
    with open(dir_memory, 'r') as f:
        m = json.load(f)
    for s in list(_get_default_memory().keys()):
        if s not in m:
            return False

    return True

# ── default memory template ───────────────────────────────────────────
def _get_default_memory():
    default_memory = {
            "CC": {},
            "AZ": {},
            "NE": {},
            "ME": {},
            }
    return default_memory


