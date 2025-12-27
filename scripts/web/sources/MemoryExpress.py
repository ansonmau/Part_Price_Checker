from selenium import webdriver
from scripts.misc.Log import MyLogger
from scripts.web.Driver import WebDriverSession
from scripts.web.Locator import Locator
import re

logger = MyLogger("Memory_Express")

class MemoryExpress:
    class locators:
        product_list = Locator('css', '[data-role="product-list-container"]')
        direct_children = Locator('css', '> *')

    def __init__(self):
        self.driver = WebDriverSession(undetected=True, headless=False)

    def scrape_price(self, item_id):
        self.item_id = item_id
        url = "https://www.memoryexpress.com/Search/Products?Search=i9-14900KF".format(item_id)
        self.driver.get(url)

        price = -1
        product_list = self.driver.find.by_loc(self.locators.product_list)
        if product_list:
            children = self.driver.find.all_from_parent(product_list, self.locators.direct_children)
            if children:
                logger.debug("Product list located. {} items found".format(len(children)))
                i = 0
                for elm in children:
                    logger.to_file(self.driver.read.textFromElement(elm), file_name=f"item_{i}")
                    i+=1
        else:
            logger.debug("No products found for '{}'".format(item_id))

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
    
