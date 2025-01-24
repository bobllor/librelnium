from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .driver_base import Driver
from getpass import getpass

import time

class Login(Driver):
    '''Class used to authenticate and start a session with ServiceNow. Inherits the `Driver` class.

    If passing in values for the username and password, DO NOT use hard coded values. 
    Instead use an `.env` file to retrieve sensitive data to pass.

    Parameters
    ----------
        `username`: The username to login. Default is `None` which prompts a manual input if no value is passed.
        
        `password`: The password to login. Default is `None` which prompts a manual input if no value is passed. 
        The input for `password` is hidden.
    '''
    def __init__(self, *, username: str = None, password: str = None):
        super().__init__()
        self.user = username if username is not None else input('Enter your username: ')
        self.pw = password if password is not None else getpass('Enter your password: ')
    
    def login(self, url: str = None, *, has_frame: bool = True):
        '''Login into ServiceNow.

        For more control over frame switching, use the built-in method `switch_frames` with the driver.

        Parameters
        ----------
            `url`: Accepts a `str` and uses the driver to navigate to the given link. By default it is `None`.

        Optional Parameters
        ----------
            `has_frame`: A `bool` used to indicate that there is a frame to switch to on the page. By default it is `True`.
        '''

        if url is not None:
            self.driver.get(url)
        
        if has_frame is True:
            self.switch_frames()

        self.presence_find_element(By.ID, "user_name").send_keys(self.user)
        self.presence_find_element(By.ID, "user_password").send_keys(self.pw)
        self.presence_find_element(By.ID, "sysverb_login").click()

        self.driver.switch_to.default_content()
        
        print("Login complete.")

        # wait required due to load times for SNOW.
        time.sleep(8)