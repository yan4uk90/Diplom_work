from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


@allure.title("Проверка заголовка страницы Kinopoisk")
def test_header(driver):
    driver.get("https://hd.kinopoisk.ru/")
    element = driver.find_element(By.TAG_NAME, "h1")
    assert element.text == "Фильмы и сериалы, премиум‑телеканалы по подписке"


@allure.title("Поиск фильма по названию")
def test_search_movie_by_title(driver):
    driver.get("https://www.kinopoisk.ru/")
    search_bar = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
    search_bar.send_keys("Интерстеллар")
    search_bar.send_keys(Keys.ENTER)

    movie_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
    )
    movie_link.click()

    assert "Интерстеллар" in driver.title, "Не удалось открыть \
        страницу фильма 'Интерстеллар'"


@allure.title("Просмотр подробной информации о фильме")
def test_view_movie_details(driver):
    driver.get("https://www.kinopoisk.ru/")
    search_bar = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
    search_bar.send_keys("Интерстеллар")
    search_bar.send_keys(Keys.ENTER)

    movie_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
    )
    movie_link.click()

    movie_info = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, '[class*="styles_paragraph"]'))
    )

    assert movie_info.is_displayed(), "Подробная информация о фильме не \
        отображается"


@allure.title("Поиск фильма")
def test_get_movie(driver):
    driver.get("https://www.kinopoisk.ru/")
    search_bar = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
    search_bar.send_keys("Интерстеллар")
    search_bar.send_keys(Keys.ENTER)

    movie_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
    )
    assert movie_link.is_displayed(), "Ссылка на фильм 'Интерстеллар' не \
        отображается"


@allure.title("Проверка информации об актерах")
def test_check_actor_info(driver):
    driver.get("https://www.kinopoisk.ru/")
    # Переход на страницу фильма
    search_bar = driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
    search_bar.send_keys("Интерстеллар")
    search_bar.send_keys(Keys.ENTER)

    movie_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
    )
    movie_link.click()

    # Переход на страницу с главными ролями
    cast_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "В главных ролях"))
    )
    cast_link.click()

    # Ожидание заголовка "Актеры"
    actor_header = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((
            By.XPATH, "//a[@name='actor']/following-sibling::div[contains(\
                text(), 'Актеры')]"))
    )
    assert actor_header.is_displayed(), "Заголовок 'Актеры' не \
        отображается"
