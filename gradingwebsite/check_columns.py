import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradingwebsite.settings')
django.setup()

from django.db import connection

def get_columns(table_name):
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            return str(e)

print("core_question columns:", get_columns('core_question'))
