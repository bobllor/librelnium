from .driver import Driver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Iterable

class VTBScanner(Driver):
    def __init__(self, driver):
        '''Class used to scan for items on the Virtual Task Board (VTB) of Service Now.

        This class assumes that the driver is on the correct URL.
        
        Parameters
        ----------
            lane_xpath: str
                The HTML xpath of a lane in the VTB. 
        '''
        super().__init__(driver)
    
    def get_elements(self, search_val: str, xpaths: Iterable[str]) -> list[WebElement] | list:
        '''Returns a list of WebElements on the VTB. If none found, an empty list is returned.

        The method searches for the elements based on the value of `search_val`, and returns filtered WebElements
        containing `search_val`. It uses the XML function `contains()` to get the result, which is **case sensitive**.

        If attempting to find elements in a certain lane, the ending xpath **must be a relative xpath**.
        If an absolute xpath is used, then the search will occur for the entire page.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            xpath_str: str
                The locator value that is used to search for. This must be in a format of a
                relative path and a **XPATH**. For example, `//li[@foo="0" and @bar="0"]//a`,
                where the search is performed inside the `<a>` element.
        '''
        elements = self._iterate_element_array(By.XPATH, xpaths[:-1])
        
        if elements != None:
            elements = elements.find_elements(By.XPATH,
                f'{xpaths[-1]}[contains(text(), "{search_val}")]')
        
        return elements
    
    def get_element(self, search_val: str, xpaths = Iterable[str]) -> WebElement | None:
        '''Returns a WebElement that contains the matching text value located in the container.
        If not found, None is returned.

        It uses the XML function `contains()` to get the result, which is **case sensitive**.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            xpaths: Iterable[str]
                Any ordered iterable that contains the locator value used to search for an element.
                The iterable must be **non-zero**, and can contain any amount of locator values. If more than
                one locator value is passed, the method assumes this is a nested element and will navigate it
                accordingly. This must be in a format of a relative path and a **XPATH**.
                
                For example, [`'//li[@foo="0" and @bar="0"]', '//a'`], will find the matching `<li>` element,
                then the `<a>` element in the `<li>` element where it performs the search for the `search_val`.
        '''
        if len(xpaths) < 0:
            raise ValueError(f'Cannot have an empty iterable.')
        
        element = self._iterate_element_array(By.XPATH, xpaths[:-1])

        if element != None:
            try:
                element = element.find_element(By.XPATH,
                    f'{xpaths[-1]}[contains(text(), "{search_val}")]')
            except NoSuchElementException:
                return None
            
        return element

    def drag_task(self, search_val: str):
        '''Drags the task over to a desired swim lane on the VTB.'''
        pass