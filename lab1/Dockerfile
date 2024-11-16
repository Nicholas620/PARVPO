# Используем базовый образ на основе Alpine
FROM alpine:latest

# Обновляем пакетный менеджер и устанавливаем зависимости
RUN apk add --no-cache git g++ make cmake libc-dev

# Создаем рабочую директорию
WORKDIR /app

# Клонируем репозиторий
RUN git clone https://github.com/Nicholas620/PARVPO.git .

# Переходим в каталог lab1
WORKDIR /app/lab1

# Компилируем приложение
RUN g++ -std=c++17 -o particle_sim main.cpp

# Устанавливаем точку входа для контейнера
ENTRYPOINT ["./particle_sim"]
