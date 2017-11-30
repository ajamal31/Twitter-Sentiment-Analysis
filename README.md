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
##### Run the following commands in order:
1. USE tweets
2. ALTER DATABASE tweets CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
3. ALTER TABLE database_tweet CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
4. ALTER TABLE database_tweet CHANGE tweet_body tweet_body VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
5. ALTER TABLE database_tweet CHANGE name name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
6. ALTER TABLE database_tweet CHANGE screen_name screen_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
7. SET NAMES utf8mb4;
8. SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
9. SET global character_set_server=utf8;
10. SET session character_set_server=utf8;

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

Testing:

db user needs to be able to create databases. The easiest way to accomplish this is to open mysql and do the following:

GRANT ALL ON *\.\* TO dbuser@localhost;

Sentiment Analysis:

pip install vaderSentiment

If it tells you you're missing a lexicon, do the following:

python
import nltk
nltk.download()
d
vader_lexicon

Vader Licence:

The MIT License (MIT)

Copyright (c) 2016 C.J. Hutto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Vader Citation:

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

