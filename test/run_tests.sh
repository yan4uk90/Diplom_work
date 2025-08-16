#!/bin/bash

if [ "$1" == "ui" ]; then
    echo "Запуск только UI-тестов..."
    pytest tests/test_ui.py --alluredir=allure_results
elif [ "$1" == "api" ]; then
    echo "Запуск только API-тестов..."
    pytest tests/test_api.py --alluredir=allure_results
else
    echo "Запуск всех тестов..."
    pytest --alluredir=allure_results
fi

# Генерация отчета Allure
allure serve allure_results