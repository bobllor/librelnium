from .driver import Driver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class VTBScanner(Driver):
    def __init__(self, driver):
        '''Class used to scan for items on the Virtual Task Board (VTB) of Service Now.
        '''
        super().__init__(driver)
    
    def get_elements(self, search_val: str, html_elements: list[str]) -> list[WebElement] | list:
        '''Scans the VTB and returns a list of WebElements.

        Searches for the elements based on the value of `search_val`, and returns WebElements that contains
        `search_val`. It uses the XML function `contains()` to get the result.
        If attempting to find elements in a certain swim lane, the final xpath in the list **must be a relative path**.
        Absolute paths will ignore the hierarchy of the DOM and will attempt to search for all matching tags.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            html_elements: list[str]
                A list of HTML elements that matches the last element in the list. 
                This must be in a format of an **XPATH**.
        '''
        elements = self._traverse_html_elements(By.XPATH, html_elements[:-1])
        
        elements = elements.find_elements(By.XPATH,
            f'{html_elements[-1]}[contains(text(), "{search_val}")]')
        
        return elements
    
    def get_element(self, search_val: str, html_elements = list[str]) -> WebElement:
        '''Returns a WebElement that contains the matching text value located in the container.
        If not found, a `NoSuchElementException` exception is raised.

        It uses the XML function `contains()` to get the result, which is **case sensitive**.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            html_elements: list[str]
                A list that contains the HTML element used to search for an element in the DOM.
                The list must be **non-zero**, and can contain any amount of HTML elements. If more than
                one HTML element is passed, the method assumes this is a nested element and will navigate it
                accordingly. This must be in a format of a relative path and a **XPATH**.
                
                For example, [`'//li[@foo="0" and @bar="0"]', './/a'`], will find the `<li>` element,
                then the `<a>` element inside where it searches for `search_val`.
        '''
        if len(html_elements) < 0:
            raise ValueError(f'Cannot have an empty iterable.')
        
        element = self._traverse_html_elements(By.XPATH, html_elements[:-1])

        element = element.find_element(By.XPATH,
            f'{html_elements[-1]}[contains(text(), "{search_val}")]')
            
        return element

    def drag_task(self, search_val: str, *, drag_from: str, drag_to: str):
        '''Drags the task over to a desired swim lane on the VTB.'''
        pass