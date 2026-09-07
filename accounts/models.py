from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the department (e.g., Computer Science)")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Departments"


class CustomUser(AbstractUser):
    """
    Custom user model for the Online Examination Management System.
    We inherit from AbstractUser to keep Django's powerful built-in authentication 
    (passwords, hashing, login logic) but add our own custom fields necessary for an academic platform.
    """
    
    # Custom Name field to accommodate middle names
    middle_name = models.CharField(max_length=30, blank=True, null=True, help_text="Optional middle name")

    # ROLE INDICATORS (Crucial for Authorization/Security)
    # These boolean flags determine what interface the user can access.
    # True = Can draft exams, False = Student dashboard.
    is_student = models.BooleanField(default=False, help_text="Designates whether the user is a student.")
    is_teacher = models.BooleanField(default=False, help_text="Designates whether the user is a teacher.")

    # Profile Image for visual identity on dashboards
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, help_text="Student Profile Picture")

    YEAR_CHOICES = [
        (1, 'First Year / Freshman'),
        (2, 'Second Year / Sophomore'),
        (3, 'Third Year / Junior'),
        (4, 'Fourth Year / Senior'),
    ]

    # ADDITIONAL STUDENT METADATA
    # student_id explicitly tracks their academic Roll Number/ID for reporting logic.
    student_id = models.CharField(max_length=20, blank=True, null=True, help_text="The university/college ID of the student.")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, help_text="The academic department this student belongs to")
    year_of_study = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    semester = models.IntegerField(choices=SEMESTER_CHOICES, blank=True, null=True, help_text="Current semester for students")
    
    # TEACHER METADATA
    subjects = models.ManyToManyField('exams.Course', blank=True, help_text="Subjects this teacher is responsible for (Teachers only).")

    def __str__(self):
        """
        String representation method.
        When this user is called in the admin UI or queries, it dynamically combines 
        their first, middle, and last names mapped against their secure username.
        """
        # filter(None) cleanly removes empty strings without throwing TypeErrors
        name_parts = filter(None, [self.first_name, self.middle_name, self.last_name])
        full_name = " ".join(name_parts)
        return f"{full_name} ({self.username})" if full_name else self.username
