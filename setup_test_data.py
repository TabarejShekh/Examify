import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from exams.models import Course

User = get_user_model()

# Create standard admin
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created with password 'admin123'")

# Create a sample teacher
if not User.objects.filter(username='teacher1').exists():
    teacher1 = User.objects.create_user('teacher1', 'teacher1@example.com', 'teacher123')
    teacher1.is_teacher = True
    teacher1.first_name = "John"
    teacher1.last_name = "Doe (Teacher)"
    teacher1.save()
    print("Teacher 'teacher1' created with password 'teacher123'")

# Create a sample course
if not Course.objects.filter(name="Introduction to Computer Science").exists():
    Course.objects.create(name="Introduction to Computer Science")
    Course.objects.create(name="Advanced Mathematics")
    print("Created sample courses.")

print("Setup Complete!")
