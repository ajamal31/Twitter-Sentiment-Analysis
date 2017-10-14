# Capstone-Project

### Installing textblob

Run the following two commands:
* $ pip install -U textblob
* $ pip install TwitterAPI
* $ python -m textblob.download_corpora

(see https://textblob.readthedocs.io/en/dev/install.html for more information or other installation methods.)


# Instructions

- Install django (https://www.djangoproject.com/download/)
- Download traffic_data
- Move to the root of traffic_data (be in the same directory as manage.py)
- Run these commands in this order:
-> python manage.py migrate
-> python manage.py makemigrations database
-> python manage.py sqlmigrate database 0001
->python manage.py migrate
-> python manage.py runserver

- Note where it started the server, go there in your browser and navigate to (server)/admin.
- Type in the username and password I told you in the group chat.
- Enjoy a look at an empty database.
