from selenium.webdriver.common.by import By

ELEMENT_TYPES = {
    "id": By.ID,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "tag": By.TAG_NAME,
}

class Locator:
    def __init__(self, locator_type: str, locator: str, label:str|None=None):
        if locator_type not in ELEMENT_TYPES:
            raise ValueError("Tried to create a locator with invalid locator type: {}".format(locator_type))

        if not label:
            label = f"{locator_type}: '{locator}'"

        self.locator_type = ELEMENT_TYPES[locator_type]
        self.locator = locator 
        self.label = label

    @property
    def raw(self):
        return (self.locator_type, self.locator)

    def get(self):
        return (self.locator_type, self.locator)

    def get_type(self):
        return self.locator_type

    def get_locator(self):
        return self.locator
    
    def __str__(self):
        return self.label

