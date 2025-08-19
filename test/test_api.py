import requests
import pytest
import allure

# Переменные
baseURL = "https://api.kinopoisk.dev/v1.4"
movie_id = 1130363
invalidID = "ERROR"  # Неверный ID
headers = {
    "X-API-KEY": "P9MD4VB-3ZPMSAE-Q0A1X8J-Y44118K"
}


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме по ID через API")
@pytest.mark.parametrize("movie_id", [1130363])
# Можно добавить другие ID для тестов
def test_get_movie_info(movie_id):
    """Тест получения информации о фильме по ID"""
    url = f"{baseURL}/movie/{movie_id}"

    with allure.step("Отправка GET-запроса для получения информации о фильме"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"
#


@allure.feature("Похожие фильмы")
@allure.story("Получение списка похожих фильмов по ID через API")
@pytest.mark.parametrize("movie_id", [movie_id])
# Можно добавить другие ID для тестов
def test_get_similar_movies(movie_id):
    """Тест получения списка похожих фильмов по ID"""
    url = f"{baseURL}/movie/{movie_id}/similars"

    with allure.step("Отправка GET-запроса для получения списка похожих \
                     фильмов"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Прокатные данные")
@allure.story("Получение прокатных данных фильма по ID через API")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_movie_distributions(movie_id):
    """Тест получения прокатных данных фильма по ID"""
    url = f"{baseURL}/movie/{movie_id}/distributions"

    with allure.step("Отправка GET-запроса для получения прокатных данных \
                     фильма"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Рецензии от зрителей")
@allure.story("Получение списка рецензий от зрителей по ID фильма через API")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_movie_reviews(movie_id):
    """Тест получения списка рецензий от зрителей по ID фильма"""
    url = f"{baseURL}/movie/{movie_id}/reviews"

    with allure.step("Отправка GET-запроса для получения списка рецензий от \
                     зрителей"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме с некорректным ID")
def test_get_movie_info_invalid_id():
    """Тест получения информации о фильме с некорректным ID"""
    url = f"{baseURL}/movie/{invalidID}"

    with allure.step("Отправка GET-запроса для получения информации о фильме с\
                     некорректным ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 400"):
        assert response.status_code == 400, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме без ID")
def test_get_movie_info_no_id():
    """Тест получения информации о фильме без ID"""
    noID = ""
    url = f"{baseURL}/movie/{noID}"

    with allure.step("Отправка GET-запроса для получения информации о фильме \
                     без ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 400"):
        assert response.status_code == 400, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Прокатные данные фильма")
@allure.story("Получение прокатных данных фильма с использованием неверного \
              метода")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_distributions_invalid_method(movie_id):
    """Тест получения прокатных данных фильма с использованием неверного \
        метода"""
    url = f"{baseURL}/movie/{movie_id}/distributions"

    with allure.step("Отправка POST-запроса для получения прокатных данных \
                     фильма"):
        response = requests.post(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 500"):
        assert response.status_code == 404, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме по ID без авторизации")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_movie_info_without_auth(movie_id):
    """Тест получения информации о фильме по ID без авторизации"""
    url = f"{baseURL}/movie/{movie_id}"

    with allure.step("Отправка GET-запроса для получения информации о фильме \
                     без авторизации"):
        response = requests.get(url)  # Без токена

    with allure.step("Проверка, что статус код ответа - 401"):
        assert response.status_code == 401, f"Unexpected status code: {
            response.status_code}"


@allure.feature("Рецензии на фильм")
@allure.story("Получение списка рецензий от зрителей по неверному ID")
def test_get_reviews_invalid_id():
    """Тест получения списка рецензий от зрителей по неверному ID"""
    url = f"{baseURL}/movie/{invalidID}/reviews"

    with allure.step("Отправка GET-запроса для получения списка рецензий по \
                     неверному ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 400"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"
