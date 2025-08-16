import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function", autouse=True)
def setup():
    """
    Фикстура для создания и закрытия браузера Chrome.
    """
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(20)
    driver.get("https://www.kinopoisk.ru/")
    yield
    driver.quit()
