from time import sleep
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
        price_text_area = Locator('id', 'ProductPricing')

    def __init__(self):
        self.driver = WebDriverSession(undetected=True, headless=False)
        self.memory.load_from_file()

    def __del__(self):
        self.driver.endself()

    def scrape_price(self, item_id):
        url = "https://www.memoryexpress.com/Search/Products?Search={}".format(item_id)
        price = -1
        results = {}
        self.item_id = item_id
        self.m_item_id = self.memory.find(item_id)

        self.driver.get(url)
        sleep(1)

        if "Search" in self.driver.read.url():
            product_text_list = self._get_product_list()
            if not product_text_list:
                logger.info("No products found for '{}'".format(self.item_id))
                return price

            logger.info("Product list located. {} items found".format(len(product_text_list)))
            logger.to_file(product_text_list, 'product_list_item')

            for p in product_text_list:
                price, model = self._extract_price_and_model(p)
                results[model] = price
                logger.debug(f"Result processed:\nName: {model}\nPrice: {price}")
            logger.info(f"{len(list(results.keys()))} items successfully processed")
            logger.to_file(results, 'results')

            if not self.m_item_id:
                logger.debug("No memory found for item. Requesting from user.")
                self.m_item_id = self.memory.query(self.item_id, results)
            else:
                logger.debug(f"Item found in memory: {self.m_item_id}")

            price = results.get(self.m_item_id, -2)
        else:
            price_area = self.driver.find.by_loc(self.locators.price_text_area)
            if price_area:
                logger.debug("Price area found")
                price_txt = self.driver.read.textFromElement(price_area)
                logger.to_file(price_txt, 'price_text')
                price = self._extract_price(price_txt)
            else:
                logger.debug("Price area not found (probably not a valid product)")

        logger.debug(f"Price found for '{self.item_id}': {price}")
        return price

    def _get_product_list(self) -> list:
        p_list = []
        product_list = self.driver.find.by_loc(self.locators.product_list)
        if product_list:
            children = self.driver.find.all_from_parent(product_list, self.locators.direct_children)
            if children:
                for product_text in [self.driver.read.textFromElement(x) for x in children]:
                    if product_text:
                        p_list.append(product_text)

        return p_list

    def _extract_price_and_model(self, product_text) -> tuple:
        words = self.item_id.split(' ')
        model_pattern = rf".*(\b(?:{'|'.join(words)})\b).*"
        price_pattern = r"\n\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"

        price_search = re.search(price_pattern, product_text)
        model_search = re.search(model_pattern, product_text, re.IGNORECASE)
        if price_search:
            price = price_search.group(1)
            price = float(price.replace(',', ''))
        else:
            price = float(-1)

        if model_search:
            model = model_search.group(0)
        else:
            model = ""

        return price, model

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



    
