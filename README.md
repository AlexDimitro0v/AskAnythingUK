# AskAnything
AskAnything is a project created by students of the University of Aberdeen for the year-long course **Software engineering and professional practise**.

* Alexandar Dimitrov
* Lukas Adomaitis 
* Niven Tanzer
* Robert Rankine
* Štěpán Brychta

## Setup
Requires [Python 3.x](https://www.python.org/downloads/) to run

1. Setup local postgres database in settings.py first. Example:
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
     - Download the newest version of PostgreSQL on https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
     - Set your password and remember it - you should use the same password in the settings.py file
     - Open PgAdmin (GUI) and create a new database called "ask_anything" next to the existing "postgres" database
     - Add "C:\Program Files\PostgreSQL\12\bin" to your PATH Environment System and User Variables
       - This can be done on PgAdmin4 in Preferences->Paths->Binary paths: - set PostgreSQL Binary Path variable to "C:\Program Files\PostgreSQL\12\bin" or wherever you have installed Postgres
       - Or alternatively by editing the system environment variables on your computer and adding the path
     - Download the database dbexport.pgsql file 
 
## Environment

* Linux, Python 3
* Windows, Python 3
* Mac, Python 3
