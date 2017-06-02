# kicker
A django webapp to calculate skills in 2vs.2 table soccer

## Installation/Setup
Setup a virtual environment.<br>
Install dependencies:<br>
```pip install -r requirements.txt```

Apply migrations to create required database tables:<br>
```python manage.py migrate```

## First Steps
Start the server:<br>
```python manage.py runserver```<br>
and visitisit http://127.0.0.1:8000/skills/ to see the current trueskills.

Create a database superuser:<br>
```python manage.py createsuperuser```<br>
and visit http://127.0.0.1:8000/admin/ to add players and enter game results.
