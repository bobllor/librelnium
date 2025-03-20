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
    
    def fill_fields(self, *, values_info: list[tuple[str, str, str]], sleep_time: float = 0) -> None:
        '''Fill the fields of the user on the user creaton page. The driver assumes it is
        already on the user creation page.

        This method **does not** submit an entry. Invoke the `submit` method to submit an entry.
        
        Error handling on the user creation page is not checked here. 
        Use the method `check_errors` to handle errors on the page.
        
        Parameters
        ----------
            values_info: list[tuple[str, str, str]]
                A list of tuples that are in order of (VALUE, DOM_ELEMENT, LOCATOR) where the
                VALUE will be inserted into the DOM_ELEMENT by searching the LOCATOR.
                For example: ('USER_EMAIL', 'user.email', By.ID), will insert
                'USER_EMAIL' at the DOM element with the ID 'user.email'.

            sleep_time: float
                A float used to delay each key insertion to the DOM element. By default it has
                no delay.
        '''
        for tup in values_info:
            element: WebElement = self.presence_find_element(tup[1], by=tup[2])

            if element is not None:
                element.send_keys(tup[0])

            time.sleep(sleep_time)

    def submit(self, submit_dom: str, *, locator: str = 'id') -> None:
        '''Submits the current entry on the user creation page.
        
        Parameters
        ----------
            submit_dom: str
                The DOM of the element that represents the save/submit button to
                insert the user into the database.

            by: str
                The locator used to find the element. By default it is By.ID.
        '''
        submit_element = self.presence_find_element(submit_dom, by=locator)

        submit_element.click()

    def check_errors(self, error_doms: list[str]) -> list[str]:
        '''Checks the page for errors and return a list of strings representing
        the text of the error messages.
        
        Parameters
        ----------
            error_doms: list[str]
                A list of DOM elements that represents the errors.
        '''
        errors = []

        for dom in error_doms:
            error_element: WebElement = self.presence_find_element(dom, By.CSS_SELECTOR)

            if error_element is not None:
                errors.append(error_element.text)

        return errors