from selenium import webdriver
from scripts.misc.Log import MyLogger
from scripts.web.Driver import WebDriverSession
from scripts.web.Locator import Locator
import re

logger = MyLogger("Memory_Express")

class MemoryExpress:
    class locators:
        price_text_area = Locator('id', 'ProductPricing')

    def __init__(self):
        self.driver = WebDriverSession(True, True)

    def scrape_price(self, item_id):
        url = "https://www.memoryexpress.com/Products/{}".format(item_id)
        self.driver.get(url)

        price = -1
        price_area = self.driver.find.by_loc(self.locators.price_text_area)
        if price_area:
            logger.debug("Price area found")
            price_txt = self.driver.read.textFromElement(price_area)
            price = self._extract_price(price_txt)
        else:
            logger.debug("Price area not found (probably not a valid product)")

        return price

    def _extract_price(self, price_text) -> float:
        search_pattern = r"Only\$(\d+(?:,\d{3})*\.\d{2})"

        search = re.search(search_pattern, price_text)
        if search:
            price = search.group(1)
            price = float(price.replace(',', ''))
            logger.debug("Successfully found price: {}".format(price))
        else:
            price = float(-1)
            logger.debug("Failed to find price in text:\n\"{}\"".format(price_text))

        return price
    
