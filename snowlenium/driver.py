from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
from typing import Iterable

class Driver:
    '''Base class for WebDriver related navigation and methods.'''
    def __init__(self, driver: WebDriver = None, options = None):
        self.driver = driver if driver else WebDriver()

        self.wait_time = 6
        self.driver_wait = WebDriverWait(self.driver, self.wait_time)
        
    def set_wait_timer(self, value: int = 6) -> None:
        '''Sets the wait timer for `WebDriverWait` to a given value. By default it is 6 seconds.'''
        self.wait_time = value
    
    def go_to(self, url: str) -> None:
        '''Goes to the given URL argument.'''
        if not isinstance(url, str):
            raise TypeError(f'Expected url to be type str but got {type(url)}')
        
        self.driver.get(url)
    
    def switch_frames(self, frame_name: str = 'gsft_main', *, return_default: bool = True) -> None:
        '''Switch frames on the current page.
        
        Raises a `TimeoutException` and a `NoSuchFrameException`, which keeps the frame on the default content.

        This method does NOT handle shadow roots in the DOM, it explicitly switches to the frame on a DOM without any checks.
        Manual navigation of shadow roots is required if it exists.

        For more fine control over frame switching, use the built-in WebDriver method `switch_to`.

        Parameters
        ----------
            `frame_name`: A `str` that is used as the ID to switch to the frame inside the current page.
            Default is `gsft_main`.

        Optional Parameters
        ----------
            `return_default`: A `bool` used to switch the drive back to the default content. Default is `True`.
            Use `False` if nested frame switching is required.
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
    
    def return_shadow_root(self, *, by: str = By.CSS_SELECTOR, html_elements: Iterable[str] = None) -> ShadowRoot:
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
        
        sr = self.driver.find_element(by, html_elements[0]).shadow_root
        
        if len(html_elements) > 1:
            for s_root in html_elements[1:]:
                sr = sr.find_element(by, s_root).shadow_root

        return sr
            
    
    def presence_find_element(self, value: str = None, *, by=By.ID) -> WebElement | None:
        '''Return a `WebElement` by using an expected condition and `WebDriverWait`. 
        If no element is found, return `None`.
        
        Parameters
        ----------
            value: str
                The attribute of a HTML element. This can be any `str` value that matches the locator strategy.
           
            by: str
                Locator strategy, can use the literal string equivalent or the By strategy. 
                By default it locates by `id`.
        '''
        if by is None or value is None:
            raise TypeError

        try:
            ele = self.driver_wait.until(EC.presence_of_element_located(
                (by, value)
            ))
        except TimeoutException:
            return None
        
        return ele