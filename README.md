# Workflow

## 1. Write sql migrations

run `python manage.py makemigrations <YOUR_APP_NAME> --empty` to generate empty migration file at APP/migrations/000X...py.

add sql commands to the operations list, forward_sql place your DDL queries (CREATE TABLE etc). reverse_sql should reverse its changes (just copy drop table if exists). Check accounts/migrations/0001_initial.py for example.

You can run empty migrations again to make another template (notice it adds dependencies). then do the same thing but for DML queries (check migrations in accounts for example)

Run your postgres DB (good idea to just use docker script in repo)

running `python manage.py migrate` will apply the sql commands you wrote to the current DB. (this means if you use postgres with docker, you can completely reset the DB environment if things go to shit)

## 2. Init pugsql connection pool

Simply copy the code and place in app folder as queries.py

```
import os
import pugsql
from django.conf import settings

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(APP_DIR, "sql")

# this variable can technically be any name ideally your app name
accounts_db = pugsql.module(SQL_DIR)

db_settings = settings.DATABASES["default"]
connection_url = f"postgresql+psycopg2://{db_settings.get('USER', 'postgres')}:{db_settings.get('PASSWORD', '12345')}@{db_settings.get('HOST', 'localhost')}:{db_settings.get('PORT', '5432')}/{db_settings['NAME']}"

accounts_db.connect(connection_url)
```

## 3. write pugsql 
create directory named "sql" on app dir and write sqls there

here the general tutorial
https://pugsql.org/

Here list of hints that affect return value of the sql to python code
https://pugsql.org/doc/0.1.15/pugsql/statement.html

## 4. call sql
use the accounts_db (module) to call each sql (based on the name u apply to each sql query)
