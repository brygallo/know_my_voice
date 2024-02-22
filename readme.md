# Welcome to Know my Voice application!

If you use pipenv, please change .env.example to .env and complete. Run this commands:

```
pipenv install --three
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

If you don't use pipen, please define environment variables |  show names in .env.example. Run this commands in your virtual environment:

```
pip3 (or pip) install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
