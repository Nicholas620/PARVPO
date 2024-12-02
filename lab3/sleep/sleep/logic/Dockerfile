FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Копируем локально скачанные пакеты в контейнер
COPY ./packages /app/packages

# Устанавливаем зависимости из локальной директории
RUN pip install --no-index --find-links=./packages -r requirements.txt

# Копируем весь остальной код приложения
COPY . .

# Запуск приложения
CMD ["python", "main.py"]
