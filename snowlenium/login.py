from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .driver_base import Driver
from getpass import getpass

import time

class Login(Driver):
    '''Class used to authenticate and start a session with ServiceNow.

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
    
    def login(self):
        '''
        Login into ServiceNow.
        '''
        self.switch_frames()

        self.presence_find_element(By.ID, "user_name").send_keys(self.user)
        self.presence_find_element(By.ID, "user_password").send_keys(self.pw)
        self.presence_find_element(By.ID, "sysverb_login").click()

        self.driver.switch_to.default_content()
        
        print("Login complete.")

        # wait required due to load times for SNOW.
        time.sleep(8)