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

### Convert database to a database that can support utf8mb4:

#### Run MySQL
###### Run the following commands in order:
1. USE tweets
- ALTER DATABASE tweets CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
- ALTER TABLE tweets.tweet CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
- ALTER TABLE tweets.tweet CHANGE tweet_body tweet_body VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
- SET NAMES utf8mb4;
- SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
- SET global character_set_server=utf8;
- SET session character_set_server=utf8;

#### Exit MySQL

#### Add the following in your /etc/my.cnf file. Note: If my.cnf does not exist in your /etc directory, then create it and add the following:
[client] <br />
default-character-set = utf8mb4

[mysql] <br />
default-character-set = utf8mb4

[mysqld] <br />
character-set-client-handshake = FALSE <br />
character-set-server = utf8mb4 <br />
collation-server = utf8mb4_unicode_ci
