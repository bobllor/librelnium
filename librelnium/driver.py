from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.chrome.webdriver as chrome
import selenium.webdriver.firefox.webdriver as firefox
import selenium.webdriver.edge.webdriver as edge
from selenium.webdriver.chrome.options import Options as chromeOptions

class Driver:
    '''Base class for WebDriver related navigation and methods.'''
    def __init__(self, driver: str | WebDriver = None, option_args: list[str] = None):
        '''
        Parameters
        ----------
            driver: str | WebDriver
                A string representing a WebDriver type or a `WebDriver` object. 
                If nothing is passed, it defaults to the `chrome.WebDriver`.
                Valid strings are `['chrome', 'firefox', 'edge']`.
            
            options: list[str]
                A list of strings that contain arguments to add into the options for the driver.
        '''
        if option_args is not None and not any(isinstance(option, str) for option in option_args):
            raise TypeError('Got unexpected type in option_args.')
        
        if option_args is None:
            options = chromeOptions()
            options.add_argument('--log-level=3')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--disable-logging')
        
        if driver == 'chrome' or driver is None:
            driver = chrome.WebDriver(options=options)
        elif driver == 'firefox':
            driver = firefox.WebDriver()
        elif driver == 'edge':
            driver = edge.WebDriver()
        
        self.driver = driver
        
        self.wait_time = 6
        self.driver_wait = WebDriverWait(self.driver, self.wait_time)
        self.action_driver = ActionChains(self.driver)
        
    def set_wait_timer(self, value: float | int = 6) -> None:
        '''Sets the wait timer for `WebDriverWait` to a given value. 
        Setting the wait timer will effect the time it takes to look for an element.
        By default it is 6 seconds.'''
        self.wait_time = value

        self.driver_wait = WebDriverWait(self.driver, self.wait_time)
    
    def go_to(self, url: str) -> None:
        '''Sends the driver to a URL.'''
        if not isinstance(url, str):
            raise TypeError(f'Expected url to be type str but got {type(url)}')
        
        self.driver.get(url)
    
    def switch_frames(self, frame_name: str | WebElement = 'gsft_main', *, return_default: bool = True):
        '''Switch frames on the current page. If the frame isn't found, it will remain on the default frame
        of the page.

        Parameters
        ----------
            frame_name: str | WebElement
                The name of the frame to switch to, it can be a string or a WebElement.
                By default the value is `gsft_main`.

            return_default: bool 
                Switch the drive back to the default frame of the page before switching to a new frame.
                Default is `True`.
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
        '''Returns the driver back to the default frame.'''
        self.driver.switch_to.default_content()
    
    def get_shadowroot_element(self, locator: str | By = By.CSS_SELECTOR, *, html_elements: list[str] = None) -> ShadowRoot:
        '''Returns a ShadowRoot of the last element in the list.
        
        Parameters
        ----------
            by: str | By
                Locator strategy, can use the literal string equivalent or the By strategy. 
                By default it locates by `css selector`.

            html_elements: list[str]
                Any list structure containing HTML elements that contains a shadow root.
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
    
    def navigate_shadowroot(self, locator: str | By = By.CSS_SELECTOR, html_elements: list[str] = None):
        '''Navigates the driver into a ShadowRoot that contains an iframe. This methods assumes the last
        element in the list will have an iframe.

        If attempting to search in a ShadowRoot, it is better to use `get_shadowroot_element` for the
        ShadowRoot. Shadow roots do not have an ID for the driver to switch focus to.
        
        Parameters
        ----------
            by: str | By
                Locator strategy, can use the literal string equivalent or the By strategy. 
                By default it locates by `css selector`.

            html_elements: list[str]
                Any list structure containing HTML elements that contains a shadow root.
        '''
        if not all(isinstance(element, str) for element in html_elements):
            raise TypeError(f'Got unexpected type in html_elements')

        if len(html_elements) < 1:
            raise ValueError(f'Cannot have an empty iterable, got {len(html_elements)} size')
        
        sr = self.driver.find_element(locator, html_elements[0]).shadow_root
        
        if len(html_elements) > 1:
            for s_root in html_elements[1:]:
                sr = sr.find_element(locator, s_root).shadow_root

        self.switch_frames(sr.find_element(By.CSS_SELECTOR, 'iframe'))
            
    def presence_find_element(self, locator: str | By = By.ID, value: str = None) -> WebElement:
        '''Return a `WebElement` by using an expected condition and `WebDriverWait`. 
        If no element is found, a `TimeoutException` exception is raised.
        
        Parameters
        ----------
            by: str | By
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

    def find_elements(self, locator: str | By, value: str) -> list[WebElement]:
        '''Returns a list of WebElements containing all elements matching the value.
        If none found, then an empty list is returned.'''
        return self.driver.find_elements(locator, value)
    
    def _traverse_html_elements(self, locator: str | By, html_elements: list[str]) -> WebElement:
        '''Iterate through a list and return the associated WebElement.
    
        If not found, a `NoSuchElementException` exception is raised.
        '''
        element = self.presence_find_element(locator, value=html_elements[0])

        for i in html_elements[1:]:
            element = element.find_element(locator, i)
        
        return element