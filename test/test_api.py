import time
import pytest
import requests
import allure
from requests.exceptions import RequestException


# Конфигурация API
# Базовый URL API Кинопоиска
API_URL = "https://api.kinopoisk.dev/v1.4"
# Замените на ваш действительный API-ключ
API_KEY = "P9MD4VB-3ZPMSAE-Q0A1X8J-Y44118K"


# Фикстура для создания HTTP-сессии с авторизацией
@pytest.fixture(scope="session")
def api_client():
    """Создает и настраивает HTTP-сессию с API-ключом для всех тестов"""
    session = requests.Session()
    # Добавляем заголовок авторизации
    session.headers.update({"X-API-KEY": API_KEY})
    return session


# Основной класс тестов
@allure.feature("API Testing")  # Группировка тестов в Allure отчете
@allure.severity("blocker")  # Общая важность тестов в классе
class TestKinopoiskAPI:

    @allure.title("Поиск фильма по ID")
    @allure.description("Проверка получения информации о фильме по его ID")
    def test_search_by_id(self, api_client):
        """Тест проверяет корректность получения данных фильма по ID"""
        with allure.step("Отправляем запрос на получение фильма по ID"):
            try:
                start_time = time.time()
                # Запрос фильма с ID 5687
                response = api_client.get(f"{API_URL}/movie/5687")
                # Расчет времени ответа в мс
                response_time = (time.time() - start_time) * 1000

            except RequestException as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")

        with allure.step("Проверяем результаты"):
            # Проверка времени ответа
            assert response_time < 500, f"Время отклика {response_time}ms \
                превышает 500ms"
            # Проверка статус-кода
            assert response.status_code == 200, "Неверный статус-код ответа"
            # Проверка наличия обязательных полей в ответе
            movie_data = response.json()
            assert "id" in movie_data, "Отсутствует поле id в ответе"
            assert "name" in movie_data, "Отсутствует поле name в ответе"

    @allure.title("Поиск фильма по названию")
    @allure.description("Проверка поиска фильмов по названию")
    def test_search_by_name(self, api_client):
        """Тест проверяет работу поиска фильмов по названию"""
        with allure.step("Отправляем запрос на поиск фильма"):
            try:
                start_time = time.time()
                response = api_client.get(f"{API_URL}/movie/search?query=Маска"
                                          )
                response_time = (time.time() - start_time) * 1000

            except RequestException as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")

        with allure.step("Проверяем результаты"):
            assert response_time < 500, f"Время отклика {response_time}ms \
                превышает 500ms"
            assert response.status_code == 200
            search_results = response.json()
            assert "docs" in search_results, "Отсутствует список результатов \
                поиска"
            assert len(search_results["docs"]) > 0, "Не найдено ни одного \
                фильма"

    @allure.title("Поиск фильмов по году выпуска")
    @allure.description("Проверка фильтрации фильмов по году выпуска")
    def test_search_by_year(self, api_client):
        """Тест проверяет фильтрацию фильмов по году выпуска"""
        with allure.step("Отправляем запрос на поиск по году"):
            try:
                start_time = time.time()
                response = api_client.get(f"{API_URL}/movie?year=1990")
                response_time = (time.time() - start_time) * 1000

            except RequestException as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")

        with allure.step("Проверяем результаты"):
            assert response_time < 500, f"Время отклика {response_time}ms \
                превышает 500ms"
            assert response.status_code == 200
            movies_data = response.json()
            assert all(movie["year"] == 1990 for movie in movies_data["docs"]
                       ), "Найдены фильмы не из 1990 года"

    @allure.title("Получение списка жанров")
    @allure.description("Проверка получения списка возможных жанров")
    def test_get_genres(self, api_client):
        """Тест проверяет получение списка доступных жанров"""
        with allure.step("Отправляем запрос на получение жанров"):
            try:
                start_time = time.time()
                response = api_client.get(
                    f"{API_URL}/movie/possible-values-by-field?field=genres.\
                        name")
                response_time = (time.time() - start_time) * 1000

            except RequestException as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")

        with allure.step("Проверяем результаты"):
            assert response_time < 500, f"Время отклика {response_time}ms \
                превышает 500ms"
            assert response.status_code == 200
            genres = response.json()
            assert isinstance(genres, list), "Список жанров должен быть \
                массивом"
            assert len(genres) > 0, "Список жанров пуст"
            assert "name" in genres[0], "У жанра должно быть поле name"

    @allure.title("Обработка некорректного ID")
    @allure.description("Проверка обработки запроса с несуществующим ID")
    @allure.severity("normal")  # Пониженная важность теста
    def test_invalid_id(self, api_client):
        """Тест проверяет обработку несуществующего ID фильма"""
        with allure.step("Отправляем запрос с некорректным ID"):
            try:
                start_time = time.time()
                response = api_client.get(f"{API_URL}/movie/0")
                response_time = (time.time() - start_time) * 1000

            except RequestException as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")

        with allure.step("Проверяем результаты"):
            assert response_time < 500, f"Время отклика {response_time}ms \
                превышает 500ms"
            assert response.status_code == 404, "Ожидался статус 404 для \
                несуществующего ID"

    @allure.title("Обработка некорректного года")
    @allure.description("Проверка обработки запроса с недопустимым годом")
    @allure.severity("normal")
    def test_invalid_year(self, api_client):
        """Тест проверяет обработку недопустимого значения года"""
        with allure.step("Отправляем запрос с некорректным годом"):
            try:
                start_time = time.time()
                response = api_client.get(f"{API_URL}/movie?year=9999")
                response_time = (time.time() - start_time) * 1000

            except RequestException as e:
                pytest.fail(f"Ошибка при выполнении запроса: {str(e)}")

        with allure.step("Проверяем результаты"):
            assert response_time < 500, f"Время отклика {response_time}ms \
                превышает 500ms"
            assert response.status_code == 400, "Ожидался статус 400 для \
                недопустимого года"
