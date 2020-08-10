from selenium import webdriver
from fixture.session import SessionHelper
from fixture.profile import ProfileHelper


class Application:

    def __init__(self, browser, base_url, login, password):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Неизвестный браузер %s" % browser)
        self.session = SessionHelper(self, login, password)
        self.profile = ProfileHelper(self)
        self.base_url = base_url

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)
        wd.maximize_window()

    def destroy(self):
        self.wd.quit()
