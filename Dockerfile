# тут мы спользуем официальный образ Alpine с CMake и GCC
FROM alpine:latest

# тут устанавливаем необходимые пакеты: GCC, CMake и Git
RUN apk update && apk add --no-cache \
    build-base \
    cmake \
    git \
    libstdc++ \
    && rm -rf /var/cache/apk/*

# Копируем исполняемыц код проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию нашего проекта
WORKDIR /app

# Создаем директорию для сборки и компилируем проект
RUN mkdir -p build && cd build && cmake .. && make

# Запускаем скомпилированную программу
CMD ["./build/particle_simulation"]
