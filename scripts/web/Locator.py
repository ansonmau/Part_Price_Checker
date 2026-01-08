from selenium.webdriver.common.by import By

ELEMENT_TYPES = {
    "id": By.ID,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "tag": By.TAG_NAME,
}
class Locator:
    def __init__(self, locator_type: str, locator: str, label:str|None=None):
        if not label:
            label = "{}: '{}'".format(locator_type, locator)

        self.locator_type = ELEMENT_TYPES[locator_type]
        self.locator = locator 
        self.label = label


    def get(self):
        return (self.locator_type, self.locator)

    def get_label(self):
        return self.label
    
    def __str__(self):
        return self.label

