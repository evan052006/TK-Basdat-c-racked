import os
import pugsql
from django.conf import settings

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(APP_DIR, "sql")

accounts_db = pugsql.module(SQL_DIR)

db_settings = settings.DATABASES["default"]
connection_url = f"postgresql+psycopg2://{db_settings.get('USER', 'postgres')}:{db_settings.get('PASSWORD', '12345')}@{db_settings.get('HOST', 'localhost')}:{db_settings.get('PORT', '5432')}/{db_settings['NAME']}?options=-csearch_path%3Dtiktaktuk"

accounts_db.connect(connection_url)
