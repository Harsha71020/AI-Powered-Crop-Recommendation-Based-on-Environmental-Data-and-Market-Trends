import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()   # requires Chrome & chromedriver in PATH
    driver.maximize_window()
    yield driver
    driver.quit()
