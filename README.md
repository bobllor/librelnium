# snowlenium
A Python library built around Selenium to handle browser interactions with ServiceNow.

# Usage

To get started, a login is required.

```
import snowlenium

login_driver = snowlenium.Login()

login_driver.driver.go_to('SOME_URL_HERE') # go to the specific URL
login_driver.login()
```