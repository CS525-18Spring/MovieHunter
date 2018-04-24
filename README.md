# MovieHunter
This is a movie website, using Django framework as backend, SQlite as database. Features like searching, user management, login via Facebook and recommender are implemented.

## Data and Database
We downloaded a raw movie dataset which contains 5000+ movies and features from IMDB. With movieid, we utilized python lib to collect the features we want from IMDB. Finally, we inserted about 3000 movies into database.

To make it easy to deploy, SQLite is used as database. The database file is "movie.db" in the root directory.

## Installation Instructions
1. Install Python 3, make sure to set environment variable correctly. https://www.python.org/
2. Install Django, https://docs.djangoproject.com/en/1.11/topics/install/#installing-official-release
3. Install Sklearn
4. In the teminal, input command: python manage.py runserver 8080
5. Open your web browser, input "localhost:8080"
6. P.S. If you fail running "python manage.py runserver 8080", try some other port numbers, like 8000.

However, we highly recommend you to visit our website directly with http://zijun-xu.com:8080. We deployed our server on Digital Ocean.
