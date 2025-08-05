# Указываем базовый образ
FROM python:3.13

WORKDIR /code

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файл pyproject.toml, который содержит зависимости и настройки проекта
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости проекта
# Используем Poetry для управления зависимостями
# Отключаем создание виртуального окружения, чтобы использовать системный Python
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi  --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
