# FundMeet


#### Проект представляет собой бекэнд часть сайта для знакомств по интересам (Хобби, фандомы, увлечения.)

Figma: https://www.figma.com/board/8ugMW4OS7HbkDScfhwGTku/Untitled?node-id=0-1&t=dpopiOC4Mn3xHW4C-1

## Инструкция к запуску

### *Первый запуск

1) Создать виртуальное окружение (если еще не создано)
```bash
    python -m venv .venv
```
Активация:
```bash
    source venv/Scripts/activate
```
2) Установить зависимости и фрэймворки
```bash
    pip install -r requirements.txt
```
3) Миграции
```bash
    python manage.py migrate
```
4) Создание суперпользователя (администратора)
```bash
    python manage.py createsuperuser
```
5) Запуск проекта
```bash
  python manage.py runserver 
```

### *При обновлении

1) Миграции
```bash
    python manage.py migrate
```
*При ошибке:
```bash
    rm db.sqlite3; python manage.py migrate; python manage.py createsuperuser
```
!!! Важно, все данные в базе будут утеряны
2) Запуск проекта
```bash
  python manage.py runserver 
```

### *Базовый запуск
```bash
  python manage.py runserver 
```