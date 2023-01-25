# fastapi restaurant
0. Пункты с 0 по 4 для тех, кто разворачивает проект без Docker
1. Создать и активировать виртуальное окружение
2. Установить requirements.txt
3. Создать, запустить базу данных postgres 
4. Заполнить переменную DATABASE_URL используя database данные из пункта 3.
5. На основе файла env_example сделать файлы .env и .env_test
6. Запускать приложение командой: docker-compose up --build 
7. Запускать тесты: docker-compose -f "docker-compose_test.yml" up --build
8. Перед запуском контейнеров выбирать нужное sqlalchemy.url в alembic.ini (временное решение)
9. Что бы очистить базу данных после тестов: docker-compose -f "docker-compose_test.yml" down



В директиве test файла docker-compose нужно указывать данные которые совпадают с подключенной базой, а иначе WARNING.
test: ["CMD-SHELL", "pg_isready -U postgres -d postgres"]

Если проблемы с миграциями db alembic revision --autogenerate -m 'initial' !!!

