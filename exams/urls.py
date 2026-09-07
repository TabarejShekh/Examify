from django.urls import path
from . import views

urlpatterns = [
    # Teacher URLs
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/exam/new/', views.ExamCreateView.as_view(), name='create_exam'),
    path('teacher/exam/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('teacher/exam/<int:pk>/edit/', views.ExamUpdateView.as_view(), name='edit_exam'),
    path('teacher/exam/<int:pk>/add_question/', views.add_question, name='add_question'),
    path('teacher/exam/<int:pk>/bulk_add_questions/', views.bulk_add_questions, name='bulk_add_questions'),
    path('teacher/question/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('teacher/question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('teacher/exam/<int:pk>/results/', views.view_exam_results, name='view_exam_results'),
    
    # Student URLs
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/exam/<int:pk>/take/', views.take_exam, name='take_exam'),
]
