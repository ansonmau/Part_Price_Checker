from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, SessionNotCreatedException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
import random
import os
from pathlib import Path

from scripts.misc.Log import MyLogger
from scripts.misc.Utils import ROOT
from scripts.web.Locator import Locator

logger = MyLogger("WebDriver")


def random_wait(min=0.25, max=0.75):
    time.sleep(random.uniform(min, max))

class WebDriverSession:
    def __init__(self, undetected=False, headless=False):
        self.undetected = undetected
        self.headless = headless
        self.options = None
        self.driver = None

        self._init_chrome_options()

        self._init_driver()

        self.find = find(self)
        self.click = click(self)
        self.waitFor = waitFor(self)
        self.input = input(self)
        self.filter = filter(self)
        self.read = read(self)
        self.iframe = iframe(self)
        self.tabControl = tabControl(self)
        self.select = select(self)
         
    def __del__(self):
        # UC quit will always cause errors even though it works
        # doing this is safe because it's during shutdown
        try:
            self.driver.quit()
        except:
            pass

    def _init_driver(self):
        try:
            if self.undetected:
                self.driver = uc.Chrome(options=self.options)
            else:
                self.driver = webdriver.Chrome(options=self.options)
        except SessionNotCreatedException as e:
            if e.msg:
                if "this version of chromedriver only supports" in e.msg.lower():
                    logger.critical("Chrome outdated. Please update.")
                    self.driver = None

        self.driver.maximize_window()

    def _init_chrome_options(self):
        downloadPath = os.path.abspath(ROOT / "dls")

        # set options for downloading
        prefs = {
            "download.default_directory": downloadPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }

        if self.undetected:
            self.options = uc.ChromeOptions()
        else:
            self.options = Options()

        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument("--disable-gpu") # good practice or smthn

        if self.headless:
            self.options.add_argument("--headless=new")


    def get(self, url):
        self.driver.get(url)

    def injectJS(self, script):
        self.driver.execute_script(script)

    def scrollToElement(self, element, centered=False):
        if centered:
            self.driver.execute_script("arguments[0].scrollIntoView({block: \"center\", inline: \"nearest\"});", element)
        else:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def getShadowRoot(self, shadow_root_parent):
        return self.driver.execute_script(
            "return arguments[0].shadowRoot", shadow_root_parent
        )

    def remove_element(self, element):
        self.driver.execute_script(
                "arguments[0].remove();", element
        )

    def parse_table(self, table_locator):
        body = Locator('tag', 'tbody')
        rows = Locator('tag', 'tr')
        cols = Locator('tag', 'td')

        table = []

        table_element = self.find.by_loc(table_locator)
        body_elm = self.find.from_parent(table_element, body)
        for row in self.find.all_from_parent(body_elm, rows):
            table.append(self.find.all_from_parent(row, cols))

        return table


    def endself(self):
        self.driver.quit()


class find:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def by_loc(self, locator:Locator, wait=5):
        try:
            element = WebDriverWait(self.sesh.driver, wait).until(
                EC.presence_of_element_located(locator.get())
            )
        except NoSuchElementException:
            logger.debug("could not find {}".format(locator))
            element = None
        except TimeoutException:
            logger.debug("timed out finding {}".format(locator))
            element = None

        return element

    def from_parent(self, parentElement, locator, wait=5):
        assert parentElement is not None
        try:
            element = WebDriverWait(self.sesh.driver, wait).until(
                lambda d: parentElement.find_element(locator.get()[0], locator.get()[1])
            )
        except NoSuchElementException:
            logger.debug("could not find {}".format(locator))
            element = None
        except TimeoutException:
            logger.debug("timed out finding {}".format(locator))
            element = None

        return element

    def all(self, locator, wait=5):
        try:
            elements = WebDriverWait(self.sesh.driver, wait).until(
                EC.presence_of_all_elements_located(locator.get())
            )
        except NoSuchElementException:
            logger.debug("could not find {}".format(locator))
            elements = None
        except TimeoutException:
            logger.debug("timed out finding {}".format(locator))
            elements = None

        return elements

    def all_from_parent(self, parentElement, locator, wait=5):
        assert parentElement is not None
        try:
            elements = WebDriverWait(self.sesh.driver, wait).until(
                lambda d: parentElement.find_elements(locator.get()[0], locator.get()[1])
            )
        except NoSuchElementException:
            logger.debug("No element {}".format(locator))
            elements = []
        except TimeoutException:
            logger.debug("Timed out finding {}".format(locator))
            elements = []

        return elements

    def links_within(self, parent_element, filter=None, wait=5):
        assert parent_element is not None

        link_loc = Locator("tag", "a", "links")
        link_elements = self.all_from_parent(parent_element, link_loc)

        if not filter:
            return link_elements

        filtered_elements = []
        for elmnt in link_elements:
            if filter in self.sesh.read.textFromElement(elmnt):
                filtered_elements.append(elmnt)

        return filtered_elements

    def buttons_within(self, parent_element, filter=None, wait=5) -> list:
        assert parent_element is not None

        btn_loc = Locator('tag', 'button', 'buttons')
        btn_elm_list = self.all_from_parent(parent_element, btn_loc)

        if not filter:
            return btn_elm_list

        filtered_elements = []
        for btn in btn_elm_list:
            if filter in self.sesh.read.textFromElement(btn):
                filtered_elements.append(btn)

        return filtered_elements

    def inputs_within(self, parent_element, filter=None, wait=5):
        assert parent_element is not None

        input_loc = Locator('tag', 'input', 'inputs')
        input_fields = self.all_from_parent(parent_element, input_loc)
        
        if not filter:
            return input_fields

        filtered_elements = []
        for field in input_fields:
            if filter in self.sesh.read.textFromElement(field):
                filtered_elements.append(field)

        return filtered_elements

    def select_list(self, locator):
        select_elm = self.sesh.find.by_loc(locator)

        return Select(select_elm)

class filter:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def byText(self, element_list, txt):
        elmnts = []
        for elmnt in element_list:
            if self.sesh.read.textFromElement(elmnt) == txt:
                elmnts.append(elmnt)
        return elmnts

    def byAttribute(self, elm_list, attribute, value):
        elmnts = []
        for elmnt in elm_list:
            if elmnt.get_attribute(attribute) == value:
                elmnts.append(elmnt)
        return elmnts
        

class waitFor:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def pageLoad(self):
        WebDriverWait(self.sesh.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def path(self, pathTuple, wait=5):
        return True if self.sesh.find.by_loc(pathTuple, wait=wait) else False

    def elementInParent(self, parent, pathTuple):
        self.sesh.find.from_parent(parent, pathTuple)

    def function(self, fnc):
        try:
            WebDriverWait(self.sesh.driver, 10).until(fnc)
        except TimeoutException:
            logger.debug("waiting for function failed")
            return False

        return True

    def hardWait(self, wait_time):
        time.sleep(wait_time)


class input:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def _sendKeys(self, target_element, keys):
        assert target_element is not None

        self.sesh.click.element(target_element)
        target_element.send_keys(keys)
        random_wait()

    def element(self, element, txt):
        self._sendKeys(element, txt)

    def path(self, pathTuple, txt):
        element = self.sesh.find.by_loc(pathTuple)

        assert element is not None
        self._sendKeys(element, txt)

    def fromParent(self, parent, pathTuple, txt):
        elmnt = self.sesh.find.from_parent(parent, pathTuple)
        self._sendKeys(elmnt, txt)


class click:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def _click_element(self, target_element):
        assert target_element is not None

        target_element.click()
        random_wait()

    def element(self, elmnt):
        self._click_element(elmnt)

    def by_loc(self, locator: Locator):
        element = self.sesh.find.by_loc(locator)

        self._click_element(element)

    def fromParent(self, parent_element, locator: Locator):
        element = self.sesh.find.from_parent(parent_element, locator)

        self._click_element(element)


class read:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def text(self, targetTuple):
        element = self.sesh.find.by_loc(targetTuple)

        return self._getElementText(element)

    def textFromElement(self, element):
        return self._getElementText(element)

    def attribute(self, targetTuple, attr_name):
        elm = self.sesh.find.by_loc(targetTuple)

        return self._getElementAttribute(elm, attr_name)

    def attributeFromElement(self, elm, attr_name):
        return self._getElementAttribute(elm, attr_name)

    def url(self):
        return self.driver.current_url

    def _getElementAttribute(self, element, attribute):
        assert element is not None
        return element.get_attribute(attribute)

    def _getElementText(self, element):
        assert element is not None
        return element.text


class iframe:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def reset(self):
        self.sesh.driver.switch_to.default_content()

    def select(self, iframe_element):
        self.sesh.driver.switch_to.frame(iframe_element)


class tabControl:
    def __init__(self, sesh: WebDriverSession):
        self.sesh = sesh

    def _waitForNewTab(self, wait=5):
        curr_num_tabs = len(self.sesh.driver.window_handles)
        try:
            WebDriverWait(self.sesh.driver, wait).until(
                lambda x: len(x.window_handles) > curr_num_tabs
            )
            return True
        except TimeoutException:
            logger.debug("New tab did not appear")

        return False

    def getNumTabs(self):
        return len(self.getTabs())

    def getTabs(self):
        return self.sesh.driver.window_handles

    def getCurrentTab(self):
        return self.sesh.driver.current_window_handle

    def focusTab(self, tab):
        self.sesh.driver.switch_to.window(tab)

    def focusNewestTab(self):
        newest_tab = self.getTabs()[-1]
        self.focusTab(newest_tab)

class select:
    def __init__(self, sesh: WebDriverSession) -> None:
        self.sesh = sesh
    
    def by_text(self, select_elm, text):
        select_elm.select_by_visible_text(text) 

    def by_value(self, select_elm, attr):
        select_elm.select_by_value(attr)

    def by_index(self, select_elm, index):
        select_elm.select_by_index(index)
        
