from .driver import Driver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class VTBScanner(Driver):
    def __init__(self, driver, lane_xpath: str):
        '''Class used to scan for items on the Virtual Task Board (VTB) of Service Now.

        This class assumes that the driver is on the correct URL.
        
        Parameters
        ----------
            lane_xpath: str
                The HTML xpath of a lane in the VTB. 
        '''
        super().__init__(driver)
        self.lane_xpath = lane_xpath
    
    def get_elements(self, text_val: str, loc_val: str, *, by: str = By.XPATH) -> list[WebElement] | list[None]:
        '''Returns a list of WebElements on the VTB. If none found, an empty list is returned.

        The driver finds the elements based on the value of `text_val`, and returns the WebElements that
        contains `text_val`. It uses the XML function `contains()` to get the result. This is case sensitive.
        
        Parameters
        ----------
            text_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            loc_val: str
                The locator value that is used to search for. This must be in a format of a
                relative path. For example, `//li[@foo="0" and @bar="0"]//a`, where the driver
                is searching the `<a>` tag for the text value in the HTML element `//li`.

            by: str
                Locator strategy, can use the literal string equivalent or the By strategy. 
                By default it locates by `xpath`.
        '''
        try:
            ritm_elements = self.driver_wait.until(
                EC.presence_of_all_elements_located((by, f'{loc_val}[contains(text(), "{text_val}")]'))
            )
        except TimeoutException:
            return []
        
        return ritm_elements
    
    def get_element(self, text_val: str) -> WebElement | None:
        '''Returns a WebElement that contains the matching text value located in the container.
        If not found, None is returned.
        
        Parameters
        ----------
            url: str
                The URL of the VTB.

            text_val: str
                A `string` that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value. It is case sensitive.
        '''
        try:
            ritm_element = self.driver_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'{self.lane_xpath}//a[contains(text(), "{text_val}")]')))
        except TimeoutException:
            return None
        
        return ritm_element

    def drag_task(self, ritm: str):
        '''Drags the task over to a desired swim lane on the VTB.'''
        pass