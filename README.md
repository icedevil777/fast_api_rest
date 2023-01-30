# FastAPI Ресторан 

####
Создать и заполнить файл .env на основе .env_example
####

#### Запустить приложение
```
docker-compose up --build
```

#### Запустить тесты
```
docker-compose -f docker-compose-tests.yml up --build
```
***
Основное приложение можно запускать с тестовым как вместе, так и отдельно. 
***

#### Остановить тестовый контейнер и очистить базу данных после тестов
```
docker-compose -f docker-compose-tests.yml down
docker-compose -f docker-compose-tests.yml down --remove-orphans
```
#### Если контейнеры не останавливаются добавить флаг --remove-orphans

#### Доп команды для проекта:
```
alembic revision --autogenerate -m 'initial'
sudo docker exec -it db_test sh -c "pytest -vv"
```

#### Если изменить пользователя базы данных в .env, то рекомендуется так же изменить директиву test.

test: ```["CMD-SHELL", "pg_isready -U TEST -d TEST"]```
