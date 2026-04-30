from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_create_schema_and_ddl"),
    ]

    operations = [
        migrations.RunSQL(
            sql="SELECT 1;",
            reverse_sql="SELECT 1;",
        )
    ]
