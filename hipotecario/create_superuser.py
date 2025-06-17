from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

try:
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
        )
        print("Superuser 'admin' created successfully.")
    else:
        print("Superuser 'admin' already exists.")
        
except OperationalError:
    print("Database is not ready yet.")