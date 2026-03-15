#!/bin/bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser if none exists
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@taskmanager.com', 'admin@123')
    print('Superuser created!')
else:
    print('Superuser already exists.')
"
