from .driver import Driver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Scanner(Driver):
    def __init__(self, driver):
        '''Class used to scan for elements on a page..'''
        super().__init__(driver)
    
    def get_elements(self, search_val: str, html_elements: list[str]) -> list[WebElement] | list:
        '''Scans the page and returns a list of WebElements.

        Searches for the elements based on the value of `search_val`, and returns WebElements that contains
        `search_val`. It uses the XML function `contains()` to get the result.
        If attempting to find nested elements, the final xpath in the list **must be a relative path**.
        Absolute paths will ignore the hierarchy of the DOM and will attempt to search for all matching tags.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            html_elements: list[str]
                A list of HTML elements that are the parents to the last element in the list.
                This must be in a format of an **XPATH**.
        '''
        if len(html_elements) == 0:
            raise ValueError('Cannot have an empty list for html_elements')

        # ignore the last element in the list, it is where the search is performed.
        if len(html_elements) > 1:
            last_element = html_elements.pop()
            parent_element = self._traverse_html_elements(By.XPATH, html_elements)

            elements = parent_element.find_elements(By.XPATH,
            f'{last_element}[contains(text(), "{search_val}")]')
        else:
            parent_element = self.presence_find_element(By.XPATH, html_elements[-1])

            elements = self.find_elements(By.XPATH, f'.//*[contains(text(), "{search_val}")]')
        
        return elements
    
    def get_element(self, search_val: str) -> WebElement | None:
        '''Returns a WebElement that contains the matching text value located in the page.
        If not found, None is returned.

        It uses the XML function `contains()` to get the result, which is **case sensitive**.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.
        '''
        if not isinstance(search_val, str):
            raise TypeError(f'Expected search_val to be type str, instead got {type(search_val)}.')

        try:
            element = self.presence_find_element(By.XPATH,
            f'//*[contains(text(), "{search_val}")]')
        except TimeoutException:
            return None
        
        return element

    def drag(self, drag_to: str, locator: str | By = By.XPATH, search_val: str | WebElement = None):
        '''Drags tasks to a desired location on a page.
        
        Parameters
        ----------
            drag_to: str
                The location the task is dragged to.

            locator: str | By
                The locator strategy used to search for the `drag_to` string.
                By default it uses the By.XPATH strategy.

            search_val: str | WebElement
                The value that is the dragged element. A string or WebElement can be used.
                If a string is given, a search on the page for the string returns a WebElement.
        '''       
        if search_val is None:
            raise ValueError(f'Expected a type str or type WebElement for search_val')
        
        if isinstance(search_val, str):
            element = self.get_element(search_val)

            if element is None:
                raise ValueError(f'Could not find {search_val}')
        elif isinstance(search_val, WebElement):
            element = search_val
        else:
            raise TypeError(f'Expected type str or WebElement for search_val, got type {type(search_val)}')

        drag_to_element = self.presence_find_element(locator, drag_to)
        
        self.action_driver.click_and_hold(element).pause(.3)

        # the pause is necessary to wait for JS to update the new card location.
        self.action_driver.move_to_element(drag_to_element).release(drag_to_element).pause(.8)
        self.action_driver.perform()

        # TODO: javascriptexception fix by scrolling down on the page with the driver.
        # it occurs due to the element being hidden by the overflow content