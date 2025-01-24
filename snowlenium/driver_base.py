from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchFrameException

class Driver:
    '''Base class for WebDriver related navigation and methods.'''
    def __init__(self):
        self.driver = WebDriver()
        self.driver_wait = WebDriverWait(self.driver, 6)

    def go_to(self, url: str) -> None:
        '''Use the driver to go to a chosen link.'''
        if not isinstance(url, str):
            raise TypeError

        self.driver.get(url)
    
    def switch_frames(self, frame_name: str = 'gsft_main') -> None:
        '''Switch frames on the current page.
        
        Raises a `TimeoutException` and a `NoSuchFrameException`, which keeps the frame on the default content.

        Parameters
        ----------
            `frame_name`: A `str` that is used as the ID to switch to the frame inside the current page.
            Default is `gsft_main`.
        '''
        self.driver.switch_to.default_content()
        
        try:
            self.driver_wait.until(
                EC.frame_to_be_available_and_switch_to_it
                    (self.driver.switch_to.frame(frame_name))
                )
        except (TimeoutException, NoSuchFrameException):
            self.driver.switch_to.default_content()
    
    def presence_find_element(self, by=By.ID, value: str = None) -> WebElement | None:
        '''Uses `WebDriverWait` to find and return a `WebElement`.
        
        If no element is found, return `None`.
        '''
        if by is None or value is None:
            raise TypeError

        ele = self.driver_wait(EC.presence_of_element_located(
            (by, value)
        ))
        
        return ele