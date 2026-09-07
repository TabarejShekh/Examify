from django.db import models
from django.conf import settings
from exams.models import Exam

class Result(models.Model):
    """
    Result Model: Core transactional record of a completed examination.
    Stores the final computed metric score dynamically derived from 
    both positive correct answers and algorithms enforcing negative marking.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
    # Kept as FloatField explicitly to dynamically support decimal 
    # negative marking deductions (e.g. subtracting 0.25 on failure).
    score = models.FloatField(default=0.0)
    
    # Automatically timestamped when the test submission completes.
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Enforces a strict Database-Level structural constraint 
        # ensuring a student cannot manipulate APIs to take an exam twice.
        unique_together = ('student', 'exam') 

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} - Score: {self.score}/{self.exam.total_marks}"
