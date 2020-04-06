# [<img src="./main/static/img/logo.png" height="50" width="50"/>](logo.png) AskAnything
<div>
   <img src ="/main/static/img/logo.png" height="50" width="50">
   <h1 style="display: inline;">AskAnything</h1>
</div>


AskAnything is a project created by students of the University of Aberdeen for the year-long course **Software engineering and professional practise**.

* Alexandar Dimitrov
* Lukas Adomaitis 
* Niven Tanzer
* Robert Rankine
* Štěpán Brychta

## Setup
Requires [Python 3.x](https://www.python.org/downloads/) to run

1. Setup local PostgreSQL in settings.py first. Example:
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
       
2. Download and unzip or simply clone this repo
3. Open your command line and navigate to the directory of the project
4. Type ```pip install -r requirements.txt``` (to install all the dependencies)
5. Type ```python manage.py makemigrations``` (to generate SQL in order to create the tables corresponding to each class in the models.py file)
6. Type ```python manage.py migrate```        (to sync the database and create the tables in database executing the commands which have been generated by makemigrations)
7. Type ```python manage.py search_index --rebuild``` to index all of the existing feedback requests, so that ElasticSearch can work properly
8. Type ```python manage.py runserver```      (to run the website on your localhost)
     
## Environment

* Linux, Python 3
* Windows, Python 3
* Mac, Python 3
