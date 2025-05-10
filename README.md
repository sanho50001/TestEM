# Barter System

Веб-приложение на Django для обмена вещами между пользователями (бартерная система).

## Возможности
- Регистрация и аутентификация пользователей
- Создание, редактирование, удаление объявлений
- Поиск и фильтрация объявлений
- Предложения обмена между пользователями
- REST API и веб-интерфейс
- Документация API (Swagger/DRF)

## Быстрый старт

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   cd TestEM
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv TestEMVenv
   ```

3. Активируйте виртуальное окружение:
   - Windows:
     ```bash
     .\TestEMVenv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source TestEMVenv/bin/activate
     ```

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

5. Примените миграции:
   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

7. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## Docker

1. Соберите и запустите контейнер:
   ```bash
   docker-compose up --build
   ```
2. Остановить:
   ```bash
   docker-compose down
   ```

## Тесты
```bash
python manage.py test
```

## Документация API
- Swagger: `/docs/`
- DRF: `/api/` 