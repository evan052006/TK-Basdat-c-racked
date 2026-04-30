from django.db import migrations


class Migration(migrations.Migration):
    dependencies = []

    FORWARD_SQL = """
        CREATE SCHEMA IF NOT EXISTS TIKTAKTUK AUTHORIZATION postgres;
        CREATE EXTENSION IF NOT EXISTS pgcrypto;

        SET SEARCH_PATH TO TIKTAKTUK;

        CREATE TABLE IF NOT EXISTS USER_ACCOUNT (
            user_id UUID PRIMARY KEY DEFAULT uuidv7(),
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ROLE (
            role_id UUID PRIMARY KEY DEFAULT uuidv7(),
            role_name VARCHAR(50) UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ACCOUNT_ROLE (
            role_id UUID NOT NULL,
            user_id UUID NOT NULL,
            PRIMARY KEY (user_id, role_id),
            FOREIGN KEY (role_id) REFERENCES ROLE(role_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES USER_ACCOUNT(user_id) ON DELETE CASCADE
        );

        RESET SEARCH_PATH;
    """

    REVERSE_SQL = """
        SET SEARCH_PATH TO TIKTAKTUK;
        DROP TABLE IF EXISTS ACCOUNT_ROLE;
        DROP TABLE IF EXISTS ROLE;
        DROP TABLE IF EXISTS USER_ACCOUNT;
        RESET SEARCH_PATH;
    """

    operations = [migrations.RunSQL(sql=FORWARD_SQL, reverse_sql=REVERSE_SQL)]
