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
from typing import Any
import time

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
    
    def scroll_to_element(self, web_element: WebElement, *,
                          main_scroll_element: str = None,
                          tags_to_scroll: list[str] = None,
                          css_properties: list[str] = None,
                          loop_limit: int = 20
                          ):
        '''Scroll to a web element on the page.

        If a web element is not visible, then this method will invoke JavaScript functions to scroll 
        to the element automatically. If found, the driver is positioned in a way where the element
        is interactable.
        
        Parameters
        ----------
            web_element: WebElement
                The Web Element on the given page.

            main_scroll_element: str
                The main container that enables scrolling on a page. This is used if the `web_element`
                is not visible on the page. This is used as an argument for a JavaScript function,
                which returns a `boolean` if the main page is scrollable. Primarily used to check 
                if a custom container is present. 
                By default, it is None. The default target is the document `body`.

            tags_to_scroll: list[str]
                A list of element tags that represents the scrollable container.
                At most it can only contain two elements.
                A JavaScript function is executed that returns a scrollable element.
                By default, it is None. It defaults to search all `div` elements on a page.

            css_properties: list[str]
                A list of CSS properties that can be found on an element.
                At most it can only contain two elements.
                These JavaScript function looks for the values 'auto' and 'scroll' for the property.
                By default, it is None. It defaults to search for the `overflow` property on an element.

            loop_limit: int
                A number representing the maximum loop count in a JavaScript function. This is used
                only if the `web_element` is not visible.
                By default it loops 20 times.
        '''
        # check if element is visible first
        element_visible: bool = self._execute_js('return arguments[0].checkVisibility();', web_element)

        if element_visible is False:
            self._inject_script('scroll-utils/is-scrollable.js')
            
             # the body is scrollable, e.g. the scroll is normal for a page.
            is_scrollable: bool = self._execute_js('return isScrollable();', main_scroll_element)

            if is_scrollable is False:
                self._inject_script('scroll-utils/find-scrollable-element.js')
                self._inject_script('scroll-utils/scroll-until-found.js')
                
                if tags_to_scroll is None or len(tags_to_scroll) == 0:
                    tags_to_scroll = ['div']

                if css_properties is None:
                    css_properties = ['overflow' for _ in range(len(tags_to_scroll))]

                scroll_elements = []

                for i, tag in enumerate(tags_to_scroll):
                    # parameters: elementTag, property
                    scroll = self._execute_js(
                        'return findScrollableElement(arguments[0], arguments[1])',
                        tag,
                        css_properties[i]
                    )

                    scroll_elements.append(scroll)

                # the next JS function expects a value or null as an argument, if the list is 1
                # then append None to the list.
                if len(scroll_elements) != 2:
                    scroll_elements.append(None)
                
                # parameters: scrollOne, scrollTwo, webElement, loopLimit
                self._execute_js(
                    'scrollUntilFound(arguments[0], arguments[1], arguments[2], arguments[3]);',
                    *scroll_elements,
                    web_element,
                    loop_limit
                )
                
                # loop used to ensure the JS function above completes.
                for i in range(loop_limit + 3):
                    if i % 3 == 0:
                        element_found: bool = self._execute_js(
                            'return arguments[0].checkVisibility()', web_element)
                    
                    if element_found:
                        break
                    
                    time.sleep(.5)

        self._execute_js('arguments[0].scrollIntoView()', web_element)
    
    def is_visible(self, element: WebElement) -> bool:
        '''Returns True if a WebElement is inside the viewport of the driver.'''

        return self._execute_js('return arguments[0].checkVisibility()', element)

    def _inject_script(self, script_name: str):
        '''Inject a script into the current window. The path is automatically pointed to the `js_scripts`
        directory, the script_name is the directory and file name.
        
        A script must be using the Window API in order to keep it persistent in the window.
        '''
        # default location for scripts
        builder = ['librelnium/js_scripts/', script_name]

        with open(''.join(builder), 'r') as file:
            # maybe parse out comments? probably not needed in the long run.
            script = file.read()

        self._execute_js(script)
        
    def _traverse_html_elements(self, strategy: str | By, locators: list[str]) -> WebElement:
        '''Iterate through a list of locators and return the last WebElement.
    
        If not found, a `NoSuchElementException` exception is raised.
        '''
        element = self.presence_find_element(strategy, value=locators[0])

        for i in locators[1:]:
            element = element.find_element(strategy, i)
        
        return element
    
    def _execute_js(self, js: str, *args: Any) -> WebElement:
        '''Execute JavaScript in the current window.'''
        return self.driver.execute_script(js, *args)
    
    def quit(self):
        '''Terminate the session.'''
        self.driver.quit()