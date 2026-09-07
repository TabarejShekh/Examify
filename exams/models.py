from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Course Model: Acts as a central category tag for exams.
    E.g., "Data Structures", "Operating Systems".
    """
    name = models.CharField(max_length=100)
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True, help_text="Semester number (1-8)")
    
    def __str__(self):
        return f"{self.name} (Sem {self.semester})" if self.semester else self.name

class Exam(models.Model):
    """
    Exam Model: The core entity that holds parameters for a single assessment.
    It links natively to a Teacher via Foreign Key to track author ownership.
    """
    # CASCADE ON DELETE enforces referential integrity. Deleting a course deletes this exam.
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    
    # We restrict authoring to only users flagged as 'is_teacher'
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_teacher': True})
    
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, blank=True, null=True, help_text="If set, only students in this department can see and take the exam.")
    
    total_marks = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    
    # ADVANCED LOGIC FIELDS (Phase 9 integration)
    # Allows exams to be pre-scheduled rather than immediately active globally.
    scheduled_date = models.DateTimeField(null=True, blank=True, help_text="Set to schedule an exam for the future.")
    # Toggles algorithms in the grading engine (views.py)
    negative_marks = models.FloatField(default=0.0, help_text="Amount to deduct per wrong answer (e.g. 0.25)")
    shuffle_questions = models.BooleanField(default=False)
    # High-level context text that renders before taking the exam
    instructions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.course.name}"

class Question(models.Model):
    """
    Question Model: Houses the textual problem posed to the candidate.
    Links specifically to ONE Exam instance.
    """
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    section_name = models.CharField(max_length=100, default='General', help_text="Section of the exam (e.g. General, Aptitude, Technical)")
    marks = models.PositiveIntegerField(default=1)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    """
    Choice Model: The multiple-choice options tied sequentially to a Question.
    """
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    # This boolean is highly secure. It is NOT exposed directly on the HTML frontend.
    # The Python backend checks this securely to derive algorithmic scoring.
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
