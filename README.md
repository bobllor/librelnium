# librelnium
A Python library built around Selenium to make browser automation easier.

This library aims to remove a lot of the boilerplate code that is required to interact with a web page.

Before starting, it is recommended to know the basics of how XPath and CSS Selectors work.

# Usage

All classes in `librelnium` inherits from the `Driver` base class, and uses the `Driver` object's property `self.driver` as an argument.

```python
from librelnium.driver import Driver

driver = Driver('chrome')
```

Example of logging in:

```python
from librelnium.driver import Driver
from librelnium.login import Login

login_driver = Login(driver.driver)

login_driver.driver.go_to('SOME_URL_HERE') 

html_elements = {
    'user_element': ('user_name', 'id'),
    'password_element': ('user_password', 'id'),
    'login_element': ('login', 'id')
}

login_driver.login(html_elements, sleep_time=8)
```

Example of scraping data:

```python
main_container = '//div[@id="container_row_23caec60e17c4a00c2ab91d15440c5ee"]'

html_elements = [main_container, './/tr[1]', './/input[1]']

scraper = Scraper(driver.driver)

element_data = scraper.get_element_attribute('xpath', html_elements, attribute='value')
```