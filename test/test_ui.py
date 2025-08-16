from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import requests
import os


def test_example(browser):
    browser.get("https://www.kinopoisk.ru/")
    element = browser.find_element(By.TAG_NAME, "h1")
    assert element.text == "Example Domain"


@allure.feature("UI Tests for Kinopoisk")
class TestKinopoiskUI:

    @allure.title("Поиск фильма по названию")
    def test_search_movie_by_title(self):
        search_bar = self.driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys("Интерстеллар")
        search_bar.send_keys(Keys.ENTER)

        movie_link = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
        )
        movie_link.click()

        assert "Интерстеллар" in self.driver.title, "Не удалось открыть \
            страницу фильма 'Интерстеллар'"

    @allure.title("Просмотр подробной информации о фильме")
    def test_view_movie_details(self):
        search_bar = self.driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys("Интерстеллар")
        search_bar.send_keys(Keys.ENTER)

        movie_link = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
        )
        movie_link.click()

        movie_info = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "styles_paragraph__wEGPz"))
        )

        assert movie_info.is_displayed(), "Подробная информация о фильме не \
            отображается"
        print("Подробная информация о фильме:", movie_info.text)

    @allure.title("Получение постера фильма")
    def test_get_movie_poster(self):
        search_bar = self.driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys("Интерстеллар")
        search_bar.send_keys(Keys.ENTER)

        movie_link = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
        )
        movie_link.click()

        # Находим постер фильма
        poster_element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "styles_posterLink__C1HRc"))
        )
        # Получаем URL постера
        poster_url = poster_element.get_attribute("href")
        # Скачиваем постер
        response = requests.get(poster_url)

        # Проверяем, что ответ успешный
        if response.status_code == 200:
            # Путь для сохранения постера
            poster_path = os.path.join("posters", "interstellar_poster.webp")
            # Создаем директорию, если её нет
            os.makedirs("posters", exist_ok=True)

            # Сохраняем постер в формате WebP
            with open(poster_path, "wb") as file:
                file.write(response.content)  # Сохраняем постер

            # Добавляем постер как вложение в Allure в формате JPG
            allure.attach.file(poster_path, name="Интерстеллар Постер",
                               attachment_type=allure.attachment_type.JPG)

            assert os.path.exists(poster_path), "Постер фильма не был скачан"
        else:
            assert False, "Не удалось загрузить постер фильма"

    @allure.title("Сортировка фильмов по жанру")
    def test_sort_movies_by_genre(self):
        # Ожидание загрузки главной страницы
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "styles_advancedSearch__uwvnd"))
        )

        # Нажимаем на кнопку "Расширенный поиск"
        advanced_search_button = self.driver.find_element(
            By.CLASS_NAME, "styles_advancedSearch__uwvnd")
        advanced_search_button.click()

        # Ожидание загрузки страницы расширенного поиска
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "m_act[genre]"))
        )  # Ожидаем загрузки элемента с ID

        # Находим выпадающий список для выбора жанра
        genre_select = self.driver.find_element(By.ID, "m_act[genre]")
        genre_select.click()  # Кликаем на выпадающий список

        # Ожидание появления опции жанра "биография"
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.XPATH, "//option[@value='22' and text()='биография']"))
        )

        # Используем JavaScript для выбора опции "биография"
        self.driver.execute_script("arguments[0].value = '22';", genre_select)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event(\
                                   'change'))", genre_select)

        # Ожидание загрузки кнопки "поиск"
        search_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.CLASS_NAME, "el_18.submit.nice_button"))
        )
        search_button.click()

        # Ожидание загрузки результатов поиска
        results_header = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "search_results_topText"))
        )

        # Проверяем, что результаты поиска отображаются
        assert "результаты" in results_header.text, \
            "Результаты поиска не отображаются"

        # Получаем количество результатов и записываем в отчет Allure
        results_count = int(results_header.text.split()[-1])
        allure.attach(f"Количество найденных фильмов: {results_count}",
                      name="Результаты поиска",
                      attachment_type=allure.attachment_type.TEXT)

        assert results_count > 0, "Не найдено результатов для жанра \
            'биография'"

    @allure.title("Проверка информации об актерах")
    def test_check_actor_info(self):
        # Переход на страницу фильма
        search_bar = self.driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Фильмы, сериалы, персоны']")
        search_bar.send_keys("Интерстеллар")
        search_bar.send_keys(Keys.ENTER)

        movie_link = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
        )
        movie_link.click()

        # Переход на страницу с главными ролями
        cast_link = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "В главных ролях"))
        )
        cast_link.click()

        # Ожидание заголовка "Актеры"
        actor_header = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH, "//a[@name='actor']/following-sibling::div[contains(\
                    text(), 'Актеры')]"))
        )
        assert actor_header.is_displayed(), "Заголовок 'Актеры' не \
            отображается"

        # Ожидание информации об актерах
        actors = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".dub .actorInfo .name a"))
        )

        assert len(actors) > 0, "Информация об актерах не найдена"

        # Вывод информации об актерах
        for actor in actors:
            print("Актер:", actor.text)
