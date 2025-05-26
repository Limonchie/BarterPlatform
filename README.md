Платформа для обмена вещами между пользователями.(по тз)

Технологии:
- Python 3.8+
- Django 4+
- SQLite/PostgreSQL
- Docker (опционально)


Установка (без Docker)
Требования
- Python 3.8+
- pip
- Virtualenv

Шаги:
1. Клонировать репозиторий:
```bash
git clone https://github.com/Limonchie/BarterPlatform.git
cd BarterPlatform
```

Создать и активировать виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate  # Windows
```

Установить зависимости:
```bash
pip install -r requirements.txt
```

Настройка базы данных (SQLite по умолчанию):
```bash
python manage.py migrate
```

Запустить сервер:
```bash
python manage.py runserver
```

Запуск с докером

Также клонируем репозиторий и переходим в папку с проектом

Собираем и запускаем контейнер:
```bash
docker-compose up --build
```

После первого запуска выполнить миграции:
```bash
docker-compose exec web python manage.py migrate
```

Запуск тестов
Без Docker:

```bash
python manage.py test ads users
```

С Docker:
```bash
docker-compose exec web python manage.py test ads users
```
