# tests/test_get_movie_info.py
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
    url = f"{baseURL}/api/v2.1/films/{movie_id}"

    with allure.step("Отправка GET-запроса для получения информации о фильме"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа"):
        data = response.json()
        assert "data" in data, "Нет ключа 'data' в ответе"
        assert data["data"]["filmId"] == movie_id, "ID фильма в ответе не \
            совпадает с запрошенным"

    with allure.step("Проверка на наличие названия фильма на русском языке"):
        assert "nameRu" in data["data"], "Нет названия фильма на русском языке"
        assert isinstance(data["data"]["nameRu"], str), "Название фильма \
            должно быть строкой"
        allure.attach(str(data["data"]["nameRu"]), name="Название фильма",
                      attachment_type=allure.attachment_type.TEXT)


@allure.feature("Похожие фильмы")
@allure.story("Получение списка похожих фильмов по ID через API")
@pytest.mark.parametrize("movie_id", [movie_id])
# Можно добавить другие ID для тестов
def test_get_similar_movies(movie_id):
    """Тест получения списка похожих фильмов по ID"""
    url = f"{baseURL}/api/v2.2/films/{movie_id}/similars"

    with allure.step("Отправка GET-запроса для получения списка похожих \
                     фильмов"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа"):
        data = response.json()
        assert "items" in data, "Нет ключа 'items' в ответе"
        assert isinstance(data["items"], list), "Список похожих фильмов должен\
            быть списком (list)"
        allure.attach(str(len(data["items"])), name="Количество похожих \
                      фильмов", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка информации о первом похожем фильме"):
        if data["items"]:
            first_similar_movie = data["items"][0]
            assert "filmId" in first_similar_movie, "Нет 'filmId' в информации\
                о первом похожем фильме"
            assert "nameRu" in first_similar_movie, "Нет 'nameRu' в информации\
                о первом похожем фильме"
            allure.attach(str(first_similar_movie["nameRu"]), name="Название \
                          первого похожего фильма",
                          attachment_type=allure.attachment_type.TEXT)


@allure.feature("Прокатные данные")
@allure.story("Получение прокатных данных фильма по ID через API")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_movie_distributions(movie_id):
    """Тест получения прокатных данных фильма по ID"""
    url = f"{baseURL}/api/v2.2/films/{movie_id}/distributions"

    with allure.step("Отправка GET-запроса для получения прокатных данных \
                     фильма"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа"):
        data = response.json()
        assert "items" in data, "Нет ключа 'items' в ответе"
        assert isinstance(data["items"], list), "Прокатные данные должны быть \
            списком (list)"
        allure.attach(str(len(data["items"])), name="Количество прокатных \
                      записей", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка информации о первой записи проката"):
        if data["items"]:
            first_distribution = data["items"][0]
            assert "type" in first_distribution, "Нет ключа 'type' в первой \
                записи проката"
            allure.attach(str(first_distribution["type"]), name="Тип первой \
                          записи проката",
                          attachment_type=allure.attachment_type.TEXT)


@allure.feature("Рецензии от зрителей")
@allure.story("Получение списка рецензий от зрителей по ID фильма через API")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_movie_reviews(movie_id):
    """Тест получения списка рецензий от зрителей по ID фильма"""
    url = f"{baseURL}/api/v2.2/films/{movie_id}/reviews"

    with allure.step("Отправка GET-запроса для получения списка рецензий от \
                     зрителей"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 200"):
        assert response.status_code == 200, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа"):
        data = response.json()
        assert "items" in data, "Нет ключа 'items' в ответе"
        assert isinstance(data["items"], list), "Список рецензий должен быть \
            списком (list)"
        allure.attach(str(len(data["items"])), name="Количество рецензий",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка информации о первой рецензии"):
        if data["items"]:
            first_review = data["items"][0]
            assert "author" in first_review, "Нет ключа 'author' в информации \
                о первой рецензии"
            assert "date" in first_review, "Нет ключа 'date' в информации о \
                первой рецензии"
            assert "description" in first_review, "Нет ключа 'description' в \
                информации о первой рецензии"
            allure.attach(first_review["author"], name="Автор первой рецензии",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(first_review["date"], name="Дата первой рецензии",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(first_review["description"], name="Описание первой \
                          рецензии",
                          attachment_type=allure.attachment_type.TEXT)


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме с некорректным ID")
def test_get_movie_info_invalid_id():
    """Тест получения информации о фильме с некорректным ID"""
    url = f"{baseURL}/api/v2.2/films/{invalidID}"

    with allure.step("Отправка GET-запроса для получения информации о фильме с\
                     некорректным ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 400"):
        assert response.status_code == 400, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа на наличие сообщения об\
                     ошибке"):
        data = response.json()
        assert "message" in data, "В ответе отсутствует ключ 'message'"
        allure.attach(data["message"], name="Сообщение об ошибке",
                      attachment_type=allure.attachment_type.TEXT)


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме без ID")
def test_get_movie_info_no_id():
    """Тест получения информации о фильме без ID"""
    noID = ""
    url = f"{baseURL}/api/v2.2/films/{noID}"

    with allure.step("Отправка GET-запроса для получения информации о фильме \
                     без ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 400"):
        assert response.status_code == 400, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа на наличие сообщения об\
                     ошибке"):
        data = response.json()
        assert "message" in data, "В ответе отсутствует ключ 'message'"
        allure.attach(data["message"], name="Сообщение об ошибке",
                      attachment_type=allure.attachment_type.TEXT)


@allure.feature("Прокатные данные фильма")
@allure.story("Получение прокатных данных фильма с использованием неверного \
              метода")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_distributions_invalid_method(movie_id):
    """Тест получения прокатных данных фильма с использованием неверного \
        метода"""
    url = f"{baseURL}/api/v2.2/films/{movie_id}/distributions"

    with allure.step("Отправка POST-запроса для получения прокатных данных \
                     фильма"):
        response = requests.post(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 500"):
        assert response.status_code == 500, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа на наличие сообщения об\
                     ошибке"):
        data = response.json()
        assert "message" in data, "В ответе отсутствует ключ 'message'"
        allure.attach(data["message"], name="Сообщение об ошибке",
                      attachment_type=allure.attachment_type.TEXT)


@allure.feature("Информация о фильме")
@allure.story("Получение информации о фильме по ID без авторизации")
@pytest.mark.parametrize("movie_id", [movie_id])
def test_get_movie_info_without_auth(movie_id):
    """Тест получения информации о фильме по ID без авторизации"""
    url = f"{baseURL}/api/v2.2/films/{movie_id}"

    with allure.step("Отправка GET-запроса для получения информации о фильме \
                     без авторизации"):
        response = requests.get(url)  # Без токена

    with allure.step("Проверка, что статус код ответа - 401"):
        assert response.status_code == 401, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа на наличие сообщения об\
                     ошибке"):
        data = response.json()
        assert "message" in data, "В ответе отсутствует ключ 'message'"
        allure.attach(data["message"], name="Сообщение об ошибке",
                      attachment_type=allure.attachment_type.TEXT)


@allure.feature("Рецензии на фильм")
@allure.story("Получение списка рецензий от зрителей по неверному ID")
def test_get_reviews_invalid_id():
    """Тест получения списка рецензий от зрителей по неверному ID"""
    url = f"{baseURL}/api/v2.2/films/{invalidID}/reviews"

    with allure.step("Отправка GET-запроса для получения списка рецензий по \
                     неверному ID"):
        response = requests.get(url, headers=headers)

    with allure.step("Проверка, что статус код ответа - 400"):
        assert response.status_code == 400, f"Unexpected status code: {
            response.status_code}"

    with allure.step("Проверка содержимого JSON-ответа на наличие сообщения об\
                     ошибке"):
        data = response.json()
        assert "message" in data, "В ответе отсутствует ключ 'message'"
        allure.attach(data["message"], name="Сообщение об ошибке",
                      attachment_type=allure.attachment_type.TEXT)
