[![Foodgram CI/CD](https://github.com/Alexshifter/foodgram/actions/workflows/main.yml/badge.svg)](https://github.com/Alexshifter/foodgram/actions/workflows/main.yml)
[![](https://github.com/Alexshifter/foodgram/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/Alexshifter/foodgram/actions/workflows/main.yml)
#  Foodgram - продуктовый помощник для обмена рецептами любимых блюд
## Возможности Foodgram
### Для всех пользователей:
  - Регистрация пользователя в приложении;
  - Просмотр списка рецептов всех авторов;
  - Просмотр отдельного рецепта автора;
  - Просмотр списка рецептов автора;
  - Получение короткой ссылки на рецепт;
  - Фильтрация по тегам.
### Для зарегистированных пользователей:
  - Создание, редактирование, удаление рецепта;
  - Добавление, удаление аватара;
  - Смена пароля пользователя;
  - Добавление рецептов в избранное;
  - Подписка на авторов;
  - Добавление рецептов в продуктовую корзину;
  - Скачивание списка ингредиентов для покупки,сформированного на основе добавленных рецептов в продуктовую корзину;
## Локальная установка и работа с приложением
_Последующие шаги приведены дл ОС Windows 10-11 c установленным Git Bash_
Клонируйте репозиторий локально:
```
git clone git@github.com:Alexshifter/foodgram.git
```
Создайте .env: в файле укажите переменные, перечисленные в .env.example и их значения. В случае локального запуска переменная ```ALLOWED_HOST``` не применяется;
Убедитесь что Docker desktop запущен на Вашем компьтере и запустите проект:
```
docker compose -f docker-compose.local.yml
```
Проект доступен по адресу:
```http://localhost```
Выполните запуск скрипта, который применяет миграции и загружает фикстуры ингредиентов, тегов и учетной записи администратора:
```
docker compose -f docker-compose.local.yml exec backend bash ./initial_set.sh
```
Документация API доступна адресу:
```http://localhost/api/docs/```
## CI/CD практики
В проекте произведена настройка CI/CD с помощью GitHub Actions.
В директории ```.github/workflows/ ``` находится файл ```main.yml```, с помощью которого запускается следующие Actions:
- В случае ```git push``` в ветку ```main``` запускаются тесты бэкенда и прокси, собираются образы и отправляются на DockerHub, а также осуществляется деплой проекта на удаленный веб-сервер в продакшн. В случае отсутствия ошибок в telegram-бот направляется сообщение о созданном коммите и успешном деплое. 
При настройке Actions на GitHub необходимо указать следующие значения 
При настройке Actions на GitHub необходимо указать следующие значения ```Secrets```:
- DOCKER_PASSWORD - пароль на DockerHub;
- DOCKER_USERNAME - имя на DockerHub;
- HOST - адрес удаленного сервера, на котором будет развернут проект;
- POSTGRES_DB - имя базы данных PostgreSQL;
- POSTGRES_PASSWORD - пароль PostgreSQL;
- POSTGRES_USER - имя пользователя PostgreSQL;
- SSH_KEY - закрытый SSH-ключ для доступа к удаленному серверу;
- SSH_PASSPHRASE - парольная фраза ключа SSH;
- USER - логин на удаленном сервере;
- TELEGRAM_TO - ID пользователя Telegram;
- TELEGRAM_TOKEN - токен telegram-бота.
## Стек технологий
Python 3.9.13, Django 3.2.16, Django REST framework 3.12.4, PostgreSQL 13.10, Nginx 1.25.4, React, Docker, GitHub Actions
## Автор
[Alexey Pakaev](https://github.com/Alexshifter/)
## Сайт проекта
[Foodgram](https://foodgram.cloudns.be)