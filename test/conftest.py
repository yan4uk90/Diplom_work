import pytest
from selenium import webdriver


@pytest.fixture(scope="function", autouse=True)
def setup(self):
    self.driver = webdriver.Chrome()
    self.driver.implicitly_wait(20)
    self.driver.get("https://www.kinopoisk.ru/")
    yield
    self.driver.quit()
