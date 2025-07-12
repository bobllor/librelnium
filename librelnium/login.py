from .driver import Driver
from getpass import getpass

import time

class Login(Driver):
    def __init__(self, driver):
        '''Class used to login.
        Parameters
        ----------
            driver: WebDriver
                Any WebDriver.
        '''
        super().__init__(driver)
    
    def login(self,
              login_elements: dict[str, tuple[str, str] | list[str, str]],
              *,
              username: str = None,
              password: str = None,
              frame: str = None,
              sleep_time: float | int = 0):
        '''
        Parameters
        ----------
            login_elements: dict[str, tuple[str, str] | list[str, str]]
                A dictionary containing three keys: `user_ele`, `pass_ele`, `login_ele`, 
                with the values being an Iterable of strings in the order of `[LOCATOR, HTML_ELEMENT]`.

            username: str, default `None`
                Default is `None` which prompts a manual input if no value is passed.
        
            password: str
                Default is `None` which prompts a manual input if no value is passed. 
                The input for `password` is hidden.

            frame: str
                If a value is given, the driver will switch to the frame.

            sleep_time: int | float
                A timer used to delay the driver after a login. Useful if there is a delay after
                logging in. By default it has no delay.
        '''
        if not all(isinstance(k, str) for k in login_elements.keys()):
            raise TypeError('Expected str for keys in dictionary')
        
        login_info = {}

        if username is None:
            login_info['user'] = getpass('Enter your username: ')
        if password is None:
            login_info['pass'] = getpass('Enter your password: ')

        if frame is not None:
            self.switch_frames(frame)
        
        # [0] indicates the type of value, [1] is the key of the login_elements
        login_values = [
            ('user', 'user_ele'), 
            ('pass', 'password_ele'),
            ('login', 'login_ele')
        ]

        for key in login_values:
            type_ = key[0]
            value = login_elements.get(key[-1])

            if value is None:
                raise KeyError(f'Expected key {key[-1]} but got None')
            
            locator: str = value[0]
            html_element: str = value[-1]
            
            web_element = self.presence_find_element(locator, html_element)

            if type_ != 'login':
                web_element.send_keys(login_info.get(type_))
            else:
                web_element.click()

        self.switch_default_frame()

        # in case there is a page loading delay
        time.sleep(sleep_time)