from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchFrameException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from .driver import Driver
import time

class UserCreation(Driver):
    def __init__(self, driver):
        super().__init__(driver)
    
    def create_user(self, *, values_info: list[tuple[str, str, str]], submit_element: str, sleep_time: float = 0):
        '''Creates the user to add into the database. When the user is filled out, submit is clicked on.
        This method assumes that the driver is on the user creation page.

        It is important to pass the DOM elements that the driver will be interacting with.
        
        Parameters
        ----------
            values_info: list[tuple[str, str, str]]
                A list of tuples that are in order of (VALUE, DOM_ELEMENT, LOCATOR) where the
                VALUE will be inserted into the DOM_ELEMENT by searching the LOCATOR.
                For example: ('USER_EMAIL', 'user.email', By.ID), will insert
                'USER_EMAIL' at the DOM element with the ID 'user.email'.
            
            submit_element: str
                The element of the DOM that represents the save/submit button to insert
                the user into the database.

            sleep_time: float
                A float used to delay each key insertion to the DOM element. By default it has a
                no delay.
        '''
        for tup in values_info:
            element: WebElement = self.presence_find_element(tup[1], by=tup[2])

            if element is not None:
                element.send_keys(tup[0])

            time.sleep(sleep_time)