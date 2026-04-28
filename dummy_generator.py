import django
from django.conf import settings
from django.contrib.auth.hashers import make_password

settings.configure()
django.setup()


def generate_dummy_sql():
    print("INSERT INTO USER_ACCOUNT (user_id, username, password) VALUES")

    values = []
    for i in range(1, 13):
        user_id = f"00000000-0000-0000-0000-{i:012d}"
        username = f"user{i}"
        raw_password = f"pass{i}"

        hashed_password = make_password(raw_password)

        values.append(f"    ('{user_id}', '{username}', '{hashed_password}')")

    sql_output = ",\n".join(values) + ";"
    print(sql_output)


if __name__ == "__main__":
    generate_dummy_sql()
