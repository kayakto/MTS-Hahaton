## Хакатон Hack&Change
### Трек Web/DA: Сервис визуализации организационной структуры от МТС Линк
### Команда: эко-ручка

## Установка и запуск

1. Склонируйте репозиторий
```bash
git clone git@github.com:kayakto/MTS-Hahaton.git
```

2. Перейдите к проекту
```bash
cd MTS-Hahaton
```

### Запуск через Docker
1. Создайте **.env** файл со следующей структурой:
```
DEBUG=True
SECRET_KEY='django-insecure--%++b_n=^($_jic0t&5v+fp+8e0z7c$'

DATABASE_NAME=django_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres_password
DATABASE_HOST=postgres
DATABASE_PORT=5432
```

2. Выполните запуск контейнеров docker-compose:
```bash
docker-compose up -d 
```

### Используя python manage.py для разработки

1. Перейдите к бекенду
```bash
cd backend
```

2. Создайте venv
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
``` 

3. Установите зависимости
```bash
pip install -r requirements.txt
```

4. Запустите сервер
```bash
python mts_hahaton/manage.py runserver
```