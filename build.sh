#!/bin/bash

echo "Запуск сборки Docker-контейнера..."
docker-compose up -d --build

echo "Проверка базы данных..."
docker exec -it $(docker ps -qf "name=web") python -c "from service.db import start_database; start_database()"

echo "Сервис успешно запущен! Откройте http://localhost:5000 в браузере."
