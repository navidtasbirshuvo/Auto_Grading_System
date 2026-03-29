import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradingwebsite.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # 1. Drop the Zombie Table
    print("Dropping core_question table...")
    try:
        cursor.execute("DROP TABLE IF EXISTS core_question CASCADE")
        print("Dropped core_question.")
    except Exception as e:
        print(f"Error dropping table: {e}")

    # 2. Reset Migration History for core
    print("Clearing migration history for 'core'...")
    try:
        cursor.execute("DELETE FROM django_migrations WHERE app = 'core'")
        print("Cleared history.")
    except Exception as e:
        print(f"Error clearing migrations: {e}")
