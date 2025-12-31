import requests
import json 
import re
from scripts.misc.Log import MyLogger, is_debug
from scripts.misc.Utils import ROOT, create_folder
from scripts.web.Memory import Memory

logger = MyLogger("NewEgg")

class NewEgg():
    memory = Memory("NE")

    def __init__(self):
        self.item_id = ""
        self.response_text = ""
        self.debug_dir = ROOT / "logs" / "newegg"
        self.search_pattern = r'window\.__initialState__\s*=\s*(\{.*?\})</script>'
        self.memory.load_from_file()

        if is_debug():
           create_folder(self.debug_dir) 
    
    def scrape_price(self, item_id):
        self.item_id = item_id
        self.send_request()
        self.extract_json()
        return self.extract_price()

    def send_request(self):
        url = "https://www.newegg.ca/p/pl?d={}".format(self.item_id)
        r = requests.get(url)
        self.response_text = r.text

        if is_debug():
            with open(self.debug_dir / "response_{}.txt".format(self.item_id), 'w') as f:
                f.write(self.response_text)

        return self.response_text

    def extract_json(self):
        j = {}
        extract = re.search(self.search_pattern, self.response_text, re.DOTALL)
        if extract:
            m = extract.group(1)
            j = json.loads(m)
        self.response_json = j

        if is_debug():
            with open(self.debug_dir / "results_{}.json".format(self.item_id), 'w') as f:
                json.dump(self.response_json, f, indent=4)

        return self.response_json

    def extract_price(self):
        model = "NA"
        price = -1

        for prod in self.response_json['Products']:
            model = prod['ItemCell']['Model']
            logger.debug("Result found: '{}'".format(model))
            if model.lower() == self.item_id.lower():
                price = prod['ItemCell']['UnitCost']
                logger.debug("Price found for '{}': {}".format(model, price))
                break
            logger.debug("Incorrect model")

        if price == -1:
            logger.debug("Failed to find model '{}' in results".format(self.item_id))

        return price
        



