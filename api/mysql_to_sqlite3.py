import os
import sys
import django
import csv

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_redis.settings')

# Setup Django
django.setup()

# Import your model
from api.models import StudentModel   # use absolute import, not relative

# Read CSV and insert into SQLite
with open('users_20k.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        StudentModel.objects.create(
            id=int(row['id']),
            username=row['username'],
            email=row['email']
        )

print("CSV imported successfully!")
