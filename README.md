# fastapi restaurant
0. Первые 5 пунктов для тех, кто разворачивает проект без Docker
1. Создать и активировать виртуальное окружение
2. Установить requirements.txt
3. Создать, запустить базу данных postgres 
4. Заполнить переменную DATABASE_URL используя database данные из пункта 3.
5. На основе файла env_example сделать файлы .env и .env_test 
6. Запускать приложение командой docker-compose up --build 
7. Запускать тесты docker-compose -f "docker-compose_test.yml" up --build
8. Можно добавить Флаг -d для фонового режима

Если пропала db alembic revision --autogenerate -m 'initial' в докере.
