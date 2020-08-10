import pytest
import config
from fixture.application import Application

fixture = None


@pytest.fixture
def app(request):
    global fixture
    browser = config.BROWSER
    base_url = config.BASE_URL
    login = config.LOGIN
    password = config.PASSWORD
    if fixture is None:
        fixture = Application(browser=browser, base_url=base_url, login=login, password=password)
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
