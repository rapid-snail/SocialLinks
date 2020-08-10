import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SessionHelper:

    def __init__(self, app, login, password):
        self.app = app
        self.login = login
        self.password = password

    def sign_in(self, login, password):
        wd = self.app.wd
        self.app.open_home_page()
        wait = WebDriverWait(wd, 1)  # seconds
        wait.until(EC.title_is("Sign-in"))
        wd.find_element_by_css_selector("a.btn.capsbtn.signin").click()
        wait.until(EC.visibility_of(wd.find_element_by_css_selector("input#signin-login")))

        wd.find_element_by_css_selector("input#signin-login").send_keys(login)
        wd.find_element_by_css_selector("input#signin-pass").send_keys(password)

        btn = wd.find_elements_by_css_selector("form button")[0] # sign in
        btn.click()
        time.sleep(1)

    def is_signed_in(self):
        wd = self.app.wd
        try:
            wd.find_element_by_css_selector("span.userName")
            return True
        except NoSuchElementException:
            return False

    def is_signed_in_as(self, login):
        wd = self.app.wd
        if self.is_signed_in():
            wd.find_element_by_css_selector("div.dropdown button").click()
            wd.find_elements_by_css_selector("div.dropdown a")[0].click()
            profile_email = wd.find_element_by_css_selector("form input#profile-email").get_attribute("value")
            return profile_email == login
        else:
            raise Exception("User is not signed in")

    def logout(self):
        wd = self.app.wd
        if self.is_signed_in():
            wd.find_element_by_css_selector("div.dropdown button").click()
            wd.find_elements_by_css_selector("div.dropdown a")[4].click()
        else:
            raise Exception("User is not signed in")

    def get_login_and_password_invalid_feedback(self):
        wd = self.app.wd
        login_feedback = wd.find_elements_by_css_selector("div.invalid-feedback")[0].text
        password_feedback = wd.find_elements_by_css_selector("div.invalid-feedback")[1].text
        return login_feedback, password_feedback
