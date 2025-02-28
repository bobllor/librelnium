from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .driver import Driver
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
    def __init__(self, driver, *, username: str = None, password: str = None):
        super().__init__(driver)
        self.user = username if username is not None else input('Enter your username: ')
        self.pw = password if password is not None else getpass('Enter your password: ')
    
    def login(self, url: str = None, 
              *, 
              has_frame: bool = True,
              search_by: str = 'id',
              login_val: dict[str, str] = None):
        '''Login into ServiceNow.

        Parameters
        ----------
            url: str 
                Accepts a `str` and uses the driver to navigate to the given link. By default it is `None`.

            has_frame: bool
                A `bool` used to indicate that there is a frame to switch to on the page. By default it is `True`.

            search_by: str
                Used to indicate what to search the element by. By default it searches by element `id`.
                Valid options `id`, `xpath`, `link text`, `partial link text`, `name`, `tag name`,
                `class name`, and `css selector`.

            login_val: dict
                A dictionary containing three keys: `user_id`, `password_id`, `login_button`, which are the
                HTML login field elements that allows the driver to interact with the login. By default, it has
                default values of element IDs.
        '''
        if url is not None:
            self.driver.get(url)

        if login_val is None:
            login_val = {
                'user_id': 'user_name',
                'password_id': 'user_password',
                'login_button': 'sysverb_login'
            }

        if has_frame is True:
            self.switch_frames()

        user = login_val.get('user_id')
        pass_ = login_val.get('password_id')
        button = login_val.get('login_button')

        for item in [user, pass_, button]:
            if not isinstance(item, str):
                raise TypeError(f'Expected {item}, got type {type(item)}')

        self.presence_find_element(user, by=search_by).send_keys(self.user)
        self.presence_find_element(pass_, by=search_by).send_keys(self.pw)
        self.presence_find_element(button, by=search_by).click()

        self.driver.switch_to.default_content()

        # wait required due to load times for SNOW.
        time.sleep(8)