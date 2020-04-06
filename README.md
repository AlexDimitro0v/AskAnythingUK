<img align="left" height="65" width="65" src="./main/static/img/logo.png">

# AskAnything 
AskAnything is a project created by students of the University of Aberdeen for the year-long course **Software engineering and professional practise**.
* Alexandar Dimitrov
* Lukas Adomaitis 
* Niven Tanzer
* Robert Rankine
* Štěpán Brychta

##  Table of Contents
* [Overview](#AskAnything)
* [Demo](#Demo)
* [Setup](#Installation)
* [Dependencies](#Dependencies)
* [Third Party Libraries](#Third)
* [Environment](#environment)

## Demo
[![AskAnything Demo](https://media.giphy.com/media/d2ZhZTK55EA2yvTy/giphy.gif)](#)

## Installation Instructions
Requires [Python 3.x](https://www.python.org/downloads/) to run

1. Setup local PostgreSQL in the AskAnything/settings.py file first. Example:
     ```
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'ask_anything',
             'USER': 'postgres',
             'PASSWORD': 'example_password',     # Note that you should use the password you set for your DB !!!
             'HOST': '127.0.0.1',
             'PORT': '5432',
         }
     }
     ```
   - Steps
     - Download the newest version of [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
     - Set your password and remember it - you should use the same password in the settings.py file
     - Open PgAdmin (GUI) and create a new database called ```ask_anything``` next to the existing ```postgres``` database
     - Add ```C:\Program Files\PostgreSQL\12\bin``` to your PATH Environment System and User Variables
       - This can be done on PgAdmin4 in Preferences->Paths->Binary paths: - set PostgreSQL Binary Path variable to ```C:\Program Files\PostgreSQL\12\bin``` or wherever you have installed Postgres
       - Or alternatively by editing the system environment variables on your computer and adding the path
     - Download the database [dbexport.pgsql](./dbexport.pgsql) file 
     - Open and navigate your command line (terminal, bash, cmd..) to the directory where you downloaded the ```dbexport.pgsql``` file in
     - Import the database into your PostgreSQL by typing ```psql -U postgres ask_anything < dbexport.pgsql```
     
     
2. Enable ElasticSearch. If you enable it correctly, you should see something like this:
    ```
    {
       "name" : "DESKTOP-VH4ED6A",
       "cluster_name" : "elasticsearch",
       "cluster_uuid" : "VtUlVwNrT_edgms-_FjY2Q",
       "version" : {
         "number" : "7.5.2",
         "build_flavor" : "default",
         "build_type" : "zip",
         "build_hash" : "8bec50e1e0ad29dad5653712cf3bb580cd1afcdf",
         "build_date" : "2020-01-15T12:11:52.313576Z",
         "build_snapshot" : false,
         "lucene_version" : "8.3.0",
         "minimum_wire_compatibility_version" : "6.8.0",
         "minimum_index_compatibility_version" : "6.0.0-beta1"
       },
       "tagline" : "You Know, for Search"
     }
     ```
   - Steps
       - Download [ElasticSearch](https://www.elastic.co/downloads/elasticsearch?fbclid=IwAR2XbaY92npI5bsGvUCl4zK5UMS17sTKwAJrHt-69dYzC9jO26Ldyj5Lv-M)
       - Extract files from the downloaded archive, navigate your command line to the bin folder and run elasticsearch.bat by typing ```elasticsearch``` into the command line. 
       - Test that elasticsearch is working by typing ```localhost:9200``` into your browser.
       - Note: You must have at least Java8 installed to run ElasticSearch
       
3. Download and unzip or simply clone this repo
4. Open your command line and navigate to the directory of the project
5. Type ```pip install -r requirements.txt``` (to install all the dependencies)
6. Type ```python manage.py makemigrations``` (to generate SQL in order to create the tables corresponding to each class in the models.py file)
7. Type ```python manage.py migrate```        (to sync the database and create the tables in database executing the commands which have been generated by makemigrations)
8. Type ```python manage.py search_index --rebuild``` to index all of the existing feedback requests, so that ElasticSearch can work properly
9. Type ```python manage.py runserver```      (to run the website on your localhost)
    
## Dependencies
* [django](https://pypi.org/project/Django/)
* [django-crispy-forms](https://pypi.org/project/django-crispy-forms/)
* [django-multiforloop](https://pypi.org/project/django-multiforloop/)
* [pillow](https://pypi.org/project/Pillow/())
* [certifi](https://pypi.org/project/certifi/)
* [chardet](https://pypi.org/project/chardet/)
* [idna](https://pypi.org/project/idna/)
* [pytz](https://pypi.org/project/pytz/)
* [requests](https://pypi.org/project/requests/)
* [urllib3](https://pypi.org/project/urllib3/)
* [argon2-cffi](https://pypi.org/project/argon2-cffi/)
* [cffi](https://pypi.org/project/cffi/)
* [django-cleanup](https://pypi.org/project/django-cleanup/)
* [braintree](https://pypi.org/project/braintree/)
* [django-elasticsearch-dsl](https://pypi.org/project/django-elasticsearch-dsl/)
* [django-phonenumber-field](https://pypi.org/project/django-phonenumber-field/)
* [phonenumbers](https://pypi.org/project/phonenumbers/)
* [sweetify](https://pypi.org/project/sweetify/)
* [django-mailer](https://pypi.org/project/django-mailer/)
* [psycopg2](https://pypi.org/project/psycopg2/)
* [nltk](https://pypi.org/project/nltk/)
* [user-agents](https://pypi.org/project/user-agents/)
* [django-user-agents](https://pypi.org/project/django-user-agents/)
* [django-ipware](https://pypi.org/project/django-ipware/)
* [coverage](https://pypi.org/project/coverage/)
* [selenium](https://pypi.org/project/selenium/)
* [django-nose](https://pypi.org/project/django-nose/) 

**TIP**: You should use `pip install -r requirements.txt` to ensure you have all dependencies before running the application.

## Third party libraries, found in ./main/static:
* [Card.js](https://github.com/jessepollak/card) used for the checkout process
* [Cropper.min.js](https://fengyuanchen.github.io/cropperjs/) used for the profile image upload
* [JSZip.min.js](https://stuk.github.io/jszip/) used for generating and reading zip files
* [Rater.min.js](https://auxiliary.github.io/rater/) used for giving ratings/reviews

## Environment
* Linux, Python 3
* Windows, Python 3
* Mac, Python 3
