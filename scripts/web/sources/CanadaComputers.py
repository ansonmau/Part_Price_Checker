from scripts.misc.Log import MyLogger, is_debug
from scripts.misc.Utils import ROOT, create_folder
import requests
import re
import json

from scripts.web.Driver import WebDriverSession
from scripts.web.Memory import Memory

logger = MyLogger("Canada_Computers")

class CanadaComputers:
    memory = Memory("CC")

    def __init__(self):
        self._init_webdriver()
        self.memory.load_from_file()
        self.response_text = "" 
        self.item_id = ""
        self.m_item_id = ""
        self.results = {} 
        self.price = -1

    def _init_webdriver(self):
        undetected = True
        headless = True
        logger.begin_msg("Starting CC webdriver")
        self.driver = WebDriverSession(undetected, headless)
        logger.end_msg('OK')

    def scrape_price(self, item_id):
        self.item_id = item_id
        self.m_item_id = self.memory.find(item_id)
        self.results = {}
        self.response_text = ""

        logger.info(f"Scraping started for '{item_id}'")

        self.send_request()
        self.extract_results()
        self.extract_price()

        return float(self.price)

    def send_request(self):
        url = "https://www.canadacomputers.com/en/search?s={}".format(self.item_id)
        self.driver.get(url)

        self.response_text = self.driver.read.html()

        logger.info("Response text recieved")

        logger.to_file(self.response_text, 'response')


    def extract_results(self):
        search_pattern = r'gtag\("event",\s*"select_item",\s*(\{.*?\})\)'
        extract = re.findall(search_pattern, self.response_text, re.DOTALL)
        for m in extract:
            j = json.loads(m) 
            model = j["items"]["item_name"]
            price = j["items"]["price"]
            logger.to_file(j, 'result')
            self.results[model] = price

    def extract_price(self):
        result_keys = list(self.results.keys())
        if len(result_keys) == 0:
            return

        if not self.m_item_id or self.m_item_id not in self.results:
            self.m_item_id = self.memory.query(self.item_id, self.results)

        self.price = self.results[self.m_item_id]
