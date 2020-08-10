import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model.profile import Profile


class ProfileHelper:

    def __init__(self, app):
        self.app = app
        self.businesses = None
        self.countries = None

    def get_countries_names_list(self):
        wd = self.app.wd
        self.go_to_profile_page()
        options = wd.find_elements_by_css_selector("select#profile-country option")
        countries_names = []
        for i in range(len(options)):
            countries_names.append(options[i].text)
        return countries_names

    def get_dial_codes_list(self):
        wd = self.app.wd
        self.go_to_profile_page()
        options = wd.find_elements_by_css_selector("select#profile-country option")
        dial_codes = []
        for i in range(len(options)):
            dial_codes.append(options[i].get_attribute("dial"))
        return dial_codes

    def go_to_profile_page(self):
        wd = self.app.wd
        self.app.session.sign_in(self.app.session.login, self.app.session.password)
        wait = WebDriverWait(wd, 1)
        wait.until(EC.visibility_of(wd.find_element_by_css_selector("div.dropdown button")))
        wd.find_element_by_css_selector("div.dropdown button").click()
        wd.find_elements_by_css_selector("div.dropdown a")[0].click()

    def get_country_name_with_dial_code_list(self):
        wd = self.app.wd
        if self.countries is None:
            self.go_to_profile_page()
            wait = WebDriverWait(wd, 1)
            wait.until(EC.visibility_of(wd.find_element_by_css_selector("select#profile-country")))
            options = wd.find_elements_by_css_selector("select#profile-country option")
            countries = []
            for i in range(len(options)):
                countries.append({"name": options[i].text, "dial": options[i].get_attribute("dial")})
            if countries:
                self.countries = countries
        return self.countries

    def get_business_list(self):
        wd = self.app.wd
        if self.businesses is None:
            self.go_to_profile_page()
            wait = WebDriverWait(wd, 1)
            wait.until(EC.visibility_of(wd.find_element_by_css_selector("select#profile-busseg")))
            options = wd.find_elements_by_css_selector("select#profile-busseg option")
            business = []
            for i in range(len(options)):
                business.append(options[i].text)
            self.businesses = business
        return self.businesses

    def get_profile_info(self):
        wd = self.app.wd
        self.go_to_profile_page()
        name = wd.find_element_by_css_selector("input#profile-name").get_attribute("value")
        email = wd.find_element_by_css_selector("input#profile-email").get_attribute("value")
        country = Select(wd.find_element_by_css_selector("select#profile-country")).first_selected_option.text
        phone_code = wd.find_element_by_css_selector("input[placeholder='Dial code']").get_attribute("value")
        phone = wd.find_element_by_css_selector("input[placeholder='Phone']").get_attribute("value")
        business = Select(wd.find_element_by_css_selector("select#profile-busseg")).first_selected_option.text
        return Profile(name=name, email=email, country=country, phone_code=phone_code, phone=phone, business=business)

    def update(self, profile):
        wd = self.app.wd
        if profile.name is not None:
            for _ in range(len(wd.find_element_by_css_selector("input[placeholder='Your name']").get_attribute("value"))):
                wd.find_element_by_css_selector("input[placeholder='Your name']").send_keys(Keys.BACKSPACE)
            wd.find_element_by_css_selector("input[placeholder='Your name']").send_keys(profile.name)

        if profile.country is not None:
            Select(wd.find_element_by_css_selector("select#profile-country")).select_by_visible_text(profile.country)
        if profile.phone_code is not None:
            for _ in range(len(wd.find_element_by_css_selector("input[placeholder='Dial code']").get_attribute("value"))):
                wd.find_element_by_css_selector("input[placeholder='Dial code']").send_keys(Keys.BACKSPACE)
            wd.find_element_by_css_selector("input[placeholder='Dial code']").send_keys(profile.phone_code)
        if profile.phone is not None:
            wd.find_element_by_css_selector("input[placeholder='Phone']").clear()
            wd.find_element_by_css_selector("input[placeholder='Phone']").send_keys(profile.phone)
        if profile.business is not None:
            Select(wd.find_element_by_css_selector("select#profile-busseg")).select_by_visible_text(profile.business)

        wd.find_elements_by_css_selector("section.sign-form form button")[0].click()  # update button
        time.sleep(1)
        try:
            wd.find_element_by_css_selector("div.alert.alert-success")
        except NoSuchElementException:
            raise Exception("There is no 'Success' alert")
        self.app.session.logout()
