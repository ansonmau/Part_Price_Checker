from scripts.misc.Log import MyLogger, is_debug
from scripts.misc.Utils import ROOT, create_folder
import requests
import re
import json

logger = MyLogger("Canada_Computers")

class CanadaComputers:
    def __init__(self):
        self.results = []
        self.results_search_pattern = r'gtag\("event",\s*"select_item",\s*(\{.*?\})\)'
        self.debug_dir = ROOT / "logs" / "cc"

        if is_debug():
            create_folder(self.debug_dir)

    def scrape_price(self, item_id):
        self.item_id = item_id
        self.send_request()
        self.extract_results()
        return self.extract_price()

    def send_request(self):
        url = "https://www.canadacomputers.com/en/search?s={}".format(self.item_id)
        r = requests.get(url)

        self.response_text = r.text

        if is_debug():
            with open(self.debug_dir / "response_{}.txt".format(self.item_id), 'w') as f:
                f.write(self.response_text)


    def extract_results(self):
        extract = re.findall(self.results_search_pattern, self.response_text, re.DOTALL)
        self.results = [json.loads(m) for m in extract]

        if is_debug():
            with open(self.debug_dir / "results_{}.json".format(self.item_id), 'w') as f:
                for r in self.results:
                    json.dump(r, f, indent=4)

    def extract_price(self):
        if len(self.results) == 0:
            price = -1
        elif len(self.results) == 1:
            price = self.results[0]["items"]["price"]
        else:
            # pick first that isn't open box
            i = 0 
            while "open box" in self.results[i]["items"]["item_name"]:
                i+=1
            price = self.results[i]["items"]["price"]

        logger.debug("Parsed price for {}: {}".format(self.item_id, price))
        return float(price)
