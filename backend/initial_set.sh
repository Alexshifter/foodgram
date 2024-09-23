#!/bin/bash

set -e

#echo "Проверка доступности базы данных..."
#python manage.py check --database default

#echo "Применение миграций..."
#python manage.py migrate

#echo "Собираем статику бэкенда..."
#python manage.py collectstatic --noinput

#echo "Копируем статику бэкенда на volumes..."

#mkdir -p /backend_static/static/
#cp -r /app/collected_static/. /backend_static/static/

echo "Загружаем дампы ингредиентов и тегов..."
python manage.py loaddata data_ingr.json data_tags.json data_adm.json

echo "Данные успешно загружены. Проект готов к работе!"
