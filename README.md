# Diplom-work
Финальное задание по автоматизированному тестированию. Тестирование UI- и API сайта "Кинопоиск". https://www.kinopoisk.ru/.

Ссылка на финальный проект по ручному тестированию: https://yana90.yonote.ru/share/bc7a03fb-5f3e-4d08-b285-c6d28298be8f

Примечание 1: 
Инструкция для получения токена.
Для начала работы с API вам необходимо получить токен, который вы можете получить в боте [@kinopoiskdev_bot](https://t.me/kinopoiskdev_bot).
После получения токена, вам необходимо авторизоваться в документации https://kinopoisk.dev/, для этого нажмите на кнопку **Authorize** и введите токен в поле **Value**.

# pytest_ui_api_template

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект 'git clone https://github.com/yan4uk90/Diplom_work.git'
2. Установить зависимости
3. Запустить тесты 'pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'

### Стек:

1. **Python**: Основной язык программирования для написания тестов.
2. **Selenium**: Библиотека для автоматизации взаимодействия с веб-браузером.
3. **Pytest**: Фреймворк для написания и запуска тестов.
4. **Allure**: Инструмент для генерации отчетов о выполнении тестов.
5. **Requests**: Внешняя библиотека Python для работы с HTTP (HyperText Transfer Protocol)
6. **Config**: 

### Струткура:
- ./test - тесты
- ./pages - описание страниц
- ./api - хелперы для работы с API
- ./db - хелперы для работы с БД

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)

### Библиотеки (!)
- pip install pytest
- pip install selenium
- pip install webdriver-manager
- pip install allure-pytest
- pip install requests

### Форматирование кода

- Код форматируется в соответствии с PEP 8 (стиль написания кода на Python).
- Используются docstrings для документирования методов и функций.
- Все шаги теста размечаются с помощью `@allure.step` или `with allure.step` для улучшения читаемости отчетов.



