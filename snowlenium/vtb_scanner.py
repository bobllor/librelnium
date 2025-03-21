from .driver import Driver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class VTBScanner(Driver):
    def __init__(self, driver):
        '''Class used to scan for items on the Virtual Task Board (VTB) of Service Now.'''
        super().__init__(driver)
    
    def get_elements(self, search_val: str, html_elements: list[str]) -> list[WebElement] | list:
        '''Scans the VTB and returns a list of WebElements.

        Searches for the elements based on the value of `search_val`, and returns WebElements that contains
        `search_val`. It uses the XML function `contains()` to get the result.
        If attempting to find elements in a certain swim lane, the final xpath in the list **must be a relative path**.
        Absolute paths will ignore the hierarchy of the DOM and will attempt to search for all matching tags.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.

            html_elements: list[str]
                A list of HTML elements that matches the last element in the list. 
                This must be in a format of an **XPATH**.
        '''
        elements = self._traverse_html_elements(By.XPATH, html_elements[:-1])
        
        elements = elements.find_elements(By.XPATH,
            f'{html_elements[-1]}[contains(text(), "{search_val}")]')
        
        return elements
    
    def get_element(self, search_val: str) -> WebElement | None:
        '''Returns a WebElement that contains the matching text value located in the container.
        If not found, None is returned.

        It uses the XML function `contains()` to get the result, which is **case sensitive**.
        
        Parameters
        ----------
            search_val: str
                Text that can be found in the card container on the VTB. The elements returned from
                this method searches elements that contain the text value.
        '''
        if not isinstance(search_val, str):
            raise TypeError(f'Expected search_val to be type str, instead got {type(search_val)}.')

        try:
            element = self.presence_find_element(By.XPATH,
            f'//*[contains(text(), "{search_val}")]')
        except TimeoutException:
            return None
            
        return element

    def drag_task(self, search_val: str = None, web_element: WebElement = None, *, drag_to: str):
        '''Drags the task over to a desired swim lane on the VTB.
        
        Parameters
        ----------
            search_val: str
            
            web_element: WebElement

            drag_to: str
        '''
        if not isinstance(search_val, str) and search_val is not None:
            raise TypeError(f'Expected type str for search_val, got type {type(search_val)}')
        if not isinstance(web_element, WebElement) and web_element is not None:
            raise TypeError(f'Expected type WebElement for web_element, got type {type(search_val)}')
        
        if search_val is None and web_element is None:
            raise ValueError(f'Expected a value for search_val or web_element')
        
        element = self.get_element(search_val)
        
        


    '''def drag_task(self, element, *, is_inc: bool = False):
        self.__switch_frames()

        lane_path = '//li[@v-lane-index="1" and @h-lane-index="0"]' if is_inc is False else '//li[@v-lane-index="2" and @h-lane-index="0"]'
        try:
            lane = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, lane_path)))
        except TimeoutException:
            return
        

        # selects the parent of the element (div). prevents: 1. clicking on the href & 2. having a javascript no size error.
        element = element.find_element(By.XPATH, '..')

        try:
            action = ActionChains(self.driver)

            action.click_and_hold(element)

            time.sleep(1)

            action.move_to_element(lane)

            time.sleep(1)

            action.release(lane).perform()

            print('   Task dragged.')
        except StaleElementReferenceException:
            # hopefully this doesn't bite me back in the ass.
            pass
        except JavascriptException:
            # used to handle elements that are not in scroll view. should happen very rarely.
            body_element = self.driver.find_element(By.CSS_SELECTOR, 'body')
            body_element.click()
            body_element.send_keys(Keys.PAGE_DOWN)

            self.drag_task(element)
        
        self.driver.switch_to.default_content()'''