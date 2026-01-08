import logging
from datetime import datetime
import json
import itertools
import time

from scripts.misc.Utils import ROOT, create_folder

log_dir = ROOT / "logs"
save_dir = log_dir / "gen"
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

create_folder(log_dir)
create_folder(save_dir)

logging.basicConfig(
    level=logging.DEBUG,
    # format="%(asctime)s %(name)s: [%(levelname)s] %(message)s",
    format="%(name)s: [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(save_dir / "{}.log".format(time))],
)


class MyLogger:
    def __init__(self, name):
        self.name = name
        self.save_dir = ROOT / "logs" / self.name
        self.logger = logging.getLogger(self.name)
        self.in_prog = False
        self.m1 = ''

        create_folder(self.save_dir)

    @staticmethod
    def set_root_level(level):
        logging.basicConfig(level=level)

    def set_level(self, level):
        self.logger.setLevel(level)    

    def get_level(self):
        return self.logger.level
    
    def out(self, msg):
        print(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def show(self, msg):
        print(msg, end='\r')

    def begin_msg(self, msg):
        if self.in_prog:
            raise Exception("Message already in progress: '{}'".format(self.m1))

        self.in_prog = True
        msg = msg + "..."
        self.m1 = msg 

        self.show(self.m1)

        
    def end_msg(self, msg=None):
        if not self.in_prog:
            raise Exception("No messages currently in progress")

        if not msg:
            msg = "OK"

        f_msg = self.m1+msg
        self.show(f_msg)
        self.info(f_msg)
        self.in_prog = False

    def to_file(self, record, file_name="out"):
        if self.get_level() == logging.INFO:
            return

        if isinstance(record, str):
            path = self.save_dir / "{}.log".format(file_name)
            with open(path, 'w') as f:
                f.write(record)
        elif isinstance(record, dict):
            path = self.save_dir / "{}.json".format(file_name)
            with open(path, 'w') as f:
                json.dump(record, f, indent=4)
        elif isinstance(record, list):
            for i in range(len(record)):
                path = self.save_dir / "{}_{}.log".format(file_name, i)
                with open(path, 'w') as f:
                    f.write(str(record[i]))

    def get_dir(self):
        return self.save_dir

def is_debug():
    return MyLogger("").get_level() == logging.DEBUG

def disable_noisy_libs_logs():
    for noisy_lib in ["urllib3", "selenium", "botocore", "undetected_chromedriver", "uc"]:
        logging.getLogger(noisy_lib).setLevel(logging.WARNING)

