from .driver import Driver
from selenium.webdriver.common.by import By

class Scraper(Driver):
    '''Class used to scrape pages on Service Now.'''
    def __init__(self, driver):
        super().__init__(driver)

    def get_element_attribute(self, locators: list[str], by: str = By.XPATH, *, attribute: str = 'value'):
        '''Get the attribute of an HTML element.'''
        web_ele = self._traverse_locators(by, locators)

        return web_ele.get_attribute(attribute)
    
    def get_all_elements(self, locators: list[str], by: str = By.XPATH):
        '''Returns a list of elements based on the value of the last index in the list.'''
        pass