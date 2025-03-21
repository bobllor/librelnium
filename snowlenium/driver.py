from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.common.exceptions import TimeoutException, NoSuchFrameException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from typing import Iterable
import selenium.webdriver.chrome.webdriver as chrome
import selenium.webdriver.firefox.webdriver as firefox
from selenium.webdriver.chrome.options import Options as chromeOptions

class Driver:
    '''Base class for WebDriver related navigation and methods.'''
    def __init__(self, driver: WebDriver = None, option_args: list[str] = None):
        '''
        Parameters
        ----------
            driver_type: str
                A string representating a `WebDriver`. By default, it uses the chrome `WebDriver`.
                Valid options are `['chrome', 'firefox', 'edge']`.
            
            options: list[str]
                A list of strings that contain arguments to add into the options for the driver.
                By default, logging is disabled for the Chrome webdriver if `None`.
        '''
        if option_args is not None and not any(isinstance(option, str) for option in option_args):
            raise TypeError('Got unexpected type in option_args.')
        
        if option_args is None:
            options = chromeOptions()
            options.add_argument('--log-level=3')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--disable-logging')

        self.driver: WebDriver = driver if driver is not None else chrome.WebDriver(options=options)
        
        self.wait_time = 6
        self.driver_wait = WebDriverWait(self.driver, self.wait_time)
        self.action_driver = ActionChains(self.driver)
        
    def set_wait_timer(self, value: int = 6) -> None:
        '''Sets the wait timer for `WebDriverWait` to a given value. By default it is 6 seconds.'''
        self.wait_time = value
    
    def go_to(self, url: str) -> None:
        '''Goes to the given URL argument.'''
        if not isinstance(url, str):
            raise TypeError(f'Expected url to be type str but got {type(url)}')
        
        self.driver.get(url)
    
    def switch_frames(self, frame_name: str = 'gsft_main', *, return_default: bool = True):
        '''Switch frames on the current page. If the frame isn't found, it will remain on the default frame
        of the page.

        This method does not account for shadow roots inside the

        For more fine control over frame switching, use the built-in WebDriver method `switch_to`.

        Parameters
        ----------
            frame_name: str 
                A string that represents the frame ID attribute of the current page.
                By default the value is `gsft_main`.

            return_default: bool 
                Switch the drive back to the default frame of the page before switching to a new frame.
                Ensures that there is no frame before interacting with a frame. Default is `True`.
        '''
        if return_default:
            self.driver.switch_to.default_content()
        
        try:
            self.driver_wait.until(
                EC.frame_to_be_available_and_switch_to_it
                    (self.driver.switch_to.frame(frame_name))
                )
        except (TimeoutException, NoSuchFrameException):
            self.driver.switch_to.default_content()
    
    def switch_default_frame(self):
        '''Returns back to the default frame.'''
        self.driver.switch_to.default_content()
    
    def navigate_shadow_root(self, locator: str = By.CSS_SELECTOR, *, html_elements: Iterable[str] = None) -> ShadowRoot:
        '''Returns a ShadowRoot of the last element in any iterable structure.

        Navigating a DOM with shadow roots is different from directly accessing a HTML element.
        The elements inside the `html_elements` iterable must have a `#shadow-root` as its child, 
        otherwise `NoSuchElementException` is thrown.

        `html_elements` must be a minimum size 1.
        
        Parameters
        ----------
            by: str
                Locator strategy, can use the literal string equivalent or the By strategy. 
                By default it locates by `css selector`.

            html_elements: Iterable[str]
                Any ordered iterable structure containing HTML elements that contains a shadow root.
        '''
        if not any(isinstance(element, str) for element in html_elements):
            raise TypeError(f'Got unexpected type in html_elements')

        if len(html_elements) < 1:
            raise ValueError(f'Cannot have an empty iterable, got {len(html_elements)} size')
        
        sr = self.driver.find_element(locator, html_elements[0]).shadow_root
        
        if len(html_elements) > 1:
            for s_root in html_elements[1:]:
                sr = sr.find_element(locator, s_root).shadow_root

        return sr
            
    def presence_find_element(self, locator=By.ID, value: str = None) -> WebElement:
        '''Return a `WebElement` by using an expected condition and `WebDriverWait`. 
        If no element is found, a `TimeoutException` exception is raised.
        
        Parameters
        ----------
            by: str
                Locator strategy, can use the literal string equivalent or the By strategy. 
                By default it locates by `id`.

            value: str
                The attribute of a HTML element. This can be any `str` value that matches the locator strategy.
        '''
        if locator is None or value is None:
            raise TypeError

        ele = self.driver_wait.until(EC.presence_of_element_located(
            (locator, value)
        ))
        
        return ele
    
    def _traverse_html_elements(self, locator: str, html_elements: Iterable[str]) -> WebElement:
        '''Iterate an iterable structure and return the associated WebElement.
        
        If not found, a `NoSuchElementException` exception is raised.
        '''
        element = self.presence_find_element(locator, value=html_elements[0])

        for i in html_elements[1:]:
            element = element.find_element(locator, i)
        
        return element