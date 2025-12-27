import logging
from datetime import datetime

from scripts.misc.Utils import ROOT, create_folder

log_dir = ROOT / "logs"
save_dir = log_dir / "gen"
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

create_folder(log_dir)
create_folder(save_dir)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s: [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(save_dir / "{}.log".format(time))],
)


class MyLogger:
    def __init__(self, name):
        self.name = name
        create_folder(ROOT / "logs" / self.name)
        self.logger = logging.getLogger(self.name)
    
    def get_level(self):
        return self.logger.level 

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def to_file(self, txt, file_name = "out"):
        path = ROOT / "logs" / self.name / "{}.log".format(file_name)
        with open(path, 'w') as f:
            f.write(txt)


def is_debug():
    return MyLogger("").get_level() == logging.DEBUG

def disable_noisy_libs_logs():
    for noisy_lib in ["urllib3", "selenium", "botocore", "undetected_chromedriver", "uc"]:
        logging.getLogger(noisy_lib).setLevel(logging.WARNING)

