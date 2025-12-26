import re
import json
import requests

class CanadaComputers:
    def __init__(self):
        self.results = []
        self.extract_results_search_pattern = r'gtag\("event",\s*"select_item",\s*(\{.*?\})\)'
        pass

    def scrape(self, item_id):
        self.item_id = item_id

        self.send_request()
        self.extract_results()
        price = self.extract_price()

        return price


    def send_request(self):
        url = "https://www.canadacomputers.com/en/search?s={}".format(self.item_id)
        r = requests.get(url)

        self.response_text = r.text

    def extract_results(self):
        extract = re.findall(self.extract_results_search_pattern, self.response_text, re.DOTALL)
        self.results = [json.loads(m) for m in extract]

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
        return float(price)

item_id = "st4000vn006"
cc = CanadaComputers()
print(cc.scrape(item_id))










