from .driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class Scraper(Driver):
    '''Class used to scrape pages on Service Now.'''
    def __init__(self, driver):
        super().__init__(driver)

    def get_element_attribute(self, locator: str, html_elements: list[str], *, attribute: str = 'value') -> str:
        '''Get the attribute of an HTML element.'''
        web_ele = self._traverse_html_elements(locator, html_elements)

        return web_ele.get_attribute(attribute)
    
    def get_all_elements(self, locator: str, html_elements: list[str]) -> list[WebElement]:
        '''Returns a list of WebElements based on the value of the last index in the list.'''
        if len(html_elements) > 1:
            traversed_element = self._traverse_html_elements(locator, html_elements)

            return traversed_element.find_elements(locator, html_elements[-1])
        
        return self.driver.find_elements(locator, html_elements[-1])