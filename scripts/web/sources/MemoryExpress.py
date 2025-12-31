from selenium import webdriver
from scripts.misc.Log import MyLogger, is_debug
from scripts.web.Driver import WebDriverSession
from scripts.web.Locator import Locator
from scripts.web.Memory import Memory
import re

logger = MyLogger("Memory_Express")

class MemoryExpress:
    memory = Memory("ME")

    class locators:
        product_list = Locator('css', '[data-role="product-list-container"]')
        direct_children = Locator('xpath', './*')

    def __init__(self):
        self.driver = WebDriverSession(undetected=True, headless=False)
        self.memory.load_from_file()
        

    def __del__(self):
        self.driver.endself()

    def scrape_price(self, item_id):
        self.item_id = item_id
        url = "https://www.memoryexpress.com/Search/Products?Search={}".format(item_id)
        self.driver.get(url)

        price = -1

        product_list = self.driver.find.by_loc(self.locators.product_list)
        if not product_list:
            logger.debug("No products found for '{}'".format(item_id))
            return price

        children = self.driver.find.all_from_parent(product_list, self.locators.direct_children)
        if not children:
            logger.debug("No products found for '{}'".format(item_id))
            return price

        logger.debug("Product list located. {} items found".format(len(children)))

        i=0
        while i < len(children):
            product_text = self.driver.read.textFromElement(children[i])
            if not product_text:
                children.pop(i)
            else:
                logger.to_file(product_text, file_name=f"item_{i}")
            i+=1

        product_text = self.driver.read.textFromElement(children[0])
        price = self._extract_price(product_text)

        return price

    def _extract_price(self, product_text) -> float:
        search_pattern = r"\n\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"

        search = re.search(search_pattern, product_text)
        if search:
            price = search.group(1)
            price = float(price.replace(',', ''))
            logger.debug("Successfully found price: {}".format(price))
        else:
            price = float(-1)
            logger.debug("Failed to find price in text:\"{}\"".format(repr(product_text)))

        return price


    
