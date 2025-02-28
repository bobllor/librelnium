from .driver import Driver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
    
    def get_elements(self, search_val: str, xpath_str: str) -> list[WebElement] | list:
        '''Returns a list of WebElements on the VTB. If none found, an empty list is returned.

        The method searches for the elements based on the value of `search_val`, and returns filtered WebElements
        containing `search_val`. It uses the XML function `contains()` to get the result, which is **case sensitive**.
        
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
        try:
            ritm_elements = self.driver_wait.until(
                EC.presence_of_all_elements_located((By.XPATH, f'{xpath_str}[contains(text(), "{search_val}")]'))
            )
        except TimeoutException:
            return []
        
        return ritm_elements
    
    def get_element(self, search_val: str, xpath_str = str) -> WebElement | None:
        '''Returns a WebElement that contains the matching text value located in the container.
        If not found, None is returned.

        It uses the XML function `contains()` to get the result, which is **case sensitive**.
        
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
        try:
            ritm_element = self.presence_find_element(
                f'{xpath_str}[contains(text(), "{search_val}")]', by=By.XPATH)
        except TimeoutException:
            return None
        
        return ritm_element

    def drag_task(self, ritm: str):
        '''Drags the task over to a desired swim lane on the VTB.'''
        pass