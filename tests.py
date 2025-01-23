from snowlenium.core.login import Login

d = Login()

d.go_to('https://tek.service-now.com/welcome.do')
d.login()

def navigate():
    pass