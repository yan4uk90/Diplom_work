@echo off
setlocal

:: Очистка старых результатов
if exist allure_results rd /s /q allure_results
mkdir allure_results

:: Проверка параметра
if "%1"=="ui" (
    echo Запуск только UI-тестов...
    pytest tests\test_ui.py --alluredir=allure_results
) else if "%1"=="api" (
    echo Запуск только API-тестов...
    pytest tests\test_api.py --alluredir=allure_results
) else (
    echo Запуск всех тестов...
    pytest --alluredir=allure_results
)

:: Генерация отчета Allure
allure serve allure_results

endlocal