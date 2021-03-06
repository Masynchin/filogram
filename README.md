# Filogram
## Предназначение
Бот разработан для удобного хранения файлов. Файлы разделяются на категории заданые пользователем. Получать и сохранять можно не только отдельные файлы, но и целые категории
## Реализация
Основное приложение (работающее с файлами) написано на чистом Python с sqlite3 в качестве БД. Телеграм-оболочка написана на [aiogram](https://github.com/aiogram/aiogram). Также есть логирование, реализовано с помощью [loguru](https://github.com/Delgan/loguru).

В качестве оболочки проекта используется [poetry](https://github.com/python-poetry/poetry)

## Использование
### Запуск

Для запуска бота написан CLI, запускаемый командой `poetry run bot [options]`.

Опции:
- --stage: где запускается бот. Варианты: `dev` - при разработке, `prod` - в продакшене. По умолчанию - `dev`
- --use: как запускать бота. Варианты: `polling` - через поллинг, `webhook` - через вебхук. По умолчанию - `polling`

В зависимости от параметра `stage` используется разный конфиг (лежат в filogram/config.py)

### Тесты
Тесты лежат в tests/, запускаются через `poetry run pytest`.

### Переменные окружения
Переменная `STAGE` ставится сама после запуска через CLI

Обязательные:

- `BOT_TOKEN` - токен телеграм-бота

При использовании вебхука:

- `WEBHOOK_PATH`
- `WEBHOOK_URL`
- `WEBAPP_HOST`
- `WEBAPP_PORT`

[Пример их содержимого](https://github.com/aiogram/aiogram/blob/dev-2.x/examples/webhook_example.py)

Так как бот запускается через poetry, то данные переменные могут находится в файле `.env` главной директории. Для чтения переменных из данного файла должен быть подключён плагин [poetry-dotenv-plugin](https://github.com/mpeteuil/poetry-dotenv-plugin) (команда установки - `poetry plugin add poetry-dotenv-plugin`)
