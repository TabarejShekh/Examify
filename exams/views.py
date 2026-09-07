"""
examify_project/exams/views.py

This module contains the core business logic and HTTP views for the Examify platform.
It handles user dashboards, dynamic exam creation (including the Fast Paste AI parser),
real-time examination taking, and automated result calculation featuring custom
negative marking algorithms.

Developed for structural efficiency and clean MVC design in Django.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
import random
import json

from .models import Exam, Question, Choice, Course
from .forms import ExamForm
from results.models import Result

# --- TEACHER VIEWS ---

@login_required
def teacher_dashboard(request):
    """
    Renders the Teacher Analytics Dashboard.
    Validates Role-Based Access Control (RBAC) to ensure only teachers can access.
    Compiles Key Performance Indicators (KPIs) like total exams, student reach, 
    and dynamically packages JSON data for the Chart.js visual frontend.
    """
    if not getattr(request.user, 'is_teacher', False):
        messages.error(request, "Access denied. Only teachers can view this page.")
        return redirect('home')
    
    exams = Exam.objects.filter(teacher=request.user)
    total_exams = exams.count()
    
    # KPIs calculation aggregation
    results = Result.objects.filter(exam__in=exams)
    total_students = results.values('student').distinct().count()
    results_published = results.values('exam').distinct().count()
    
    now = timezone.now()
    enriched_exams = []
    for exam in exams:
        if exam.scheduled_date:
            if exam.scheduled_date > now:
                exam.status = 'Scheduled'
                exam.status_color = '#d69e2e' # Yellow/Orange
            else:
                exam.status = 'Active'
                exam.status_color = '#38a169' # Green
        else:
            exam.status = 'Active'
            exam.status_color = '#38a169'
        enriched_exams.append(exam)
    # Pass chart data to context (for dynamic frontend charts)
    chart_labels = json.dumps([exam.title for exam in enriched_exams])
    chart_data = json.dumps([Result.objects.filter(exam=exam).count() for exam in enriched_exams])
        
    context = {
        'exams': enriched_exams,
        'kpi_total_exams': total_exams,
        'kpi_total_students': total_students,
        'kpi_results_published': results_published,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'exams/teacher_dashboard.html', context)

@method_decorator(login_required, name='dispatch')
class ExamCreateView(CreateView):
    """
    Class-Based View (CBV) to handle the creation of new Exam configuration objects.
    Automatically assigns the authenticated teacher and their associated department
    to the generated exam object to prevent cross-department security flaws.
    """
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        
    def form_valid(self, form):
        # We must make sure the teacher is attached to the newly created exam
        if not getattr(self.request.user, 'is_teacher', False):
            messages.error(self.request, "Access denied.")
            return redirect('home')
        form.instance.teacher = self.request.user
        form.instance.department = self.request.user.department
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('exam_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class ExamUpdateView(UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        # Only allow the teacher who created it to edit it
        return super().get_queryset().filter(teacher=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, "Exam updated successfully.")
        return reverse_lazy('exam_detail', kwargs={'pk': self.object.pk})

@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    return render(request, 'exams/exam_detail.html', {'exam': exam})

@login_required
def add_question(request, pk):
    """
    Teacher adds a question and up to 4 choices for it.
    """
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        marks = request.POST.get('marks', 1)
        
        # Create Question
        question = Question.objects.create(exam=exam, text=question_text, marks=marks)
        
        # Create corresponding choices
        for i in range(1, 5):
            choice_text = request.POST.get(f'choice_{i}')
            # Radio button 'is_correct' passes the value of the selected radio button which we set up as str(1..4)
            is_correct = (request.POST.get('is_correct') == str(i))
            
            if choice_text:  # Only save if choice was actually typed in
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
                
        messages.success(request, "Question added successfully!")
        return redirect('exam_detail', pk=exam.pk)

    return render(request, 'exams/add_question.html', {'exam': exam})

@login_required
def edit_question(request, pk):
    """
    Teacher edits a specific question and its choices.
    """
    question = get_object_or_404(Question, pk=pk, exam__teacher=request.user)
    choices = list(question.choices.all())
    
    # Ensure exactly 4 choices are passed to the template
    while len(choices) < 4:
        choices.append(Choice(question=question, text='', is_correct=False))

    if request.method == 'POST':
        question.text = request.POST.get('question_text')
        question.section_name = request.POST.get('section_name', 'General')
        question.marks = request.POST.get('marks', 1)
        question.save()

        # Overwrite all choices to capture changes securely
        question.choices.all().delete()
        for i in range(1, 5):
            choice_text = request.POST.get(f'choice_{i}')
            is_correct = (request.POST.get('is_correct') == str(i))
            if choice_text:
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
                
        messages.success(request, "Question updated successfully!")
        return redirect('exam_detail', pk=question.exam.pk)

    return render(request, 'exams/edit_question.html', {'question': question, 'choices': choices})

@login_required
def bulk_add_questions(request, pk):
    """
    Advanced 'Fast Paste AI' parser endpoint.
    Retrieves raw text input containing multiple questions, choices, and answers
    formatted with specific syntax markers (e.g., [SECTION: X], [x], MARKS: Y).
    Parses strings securely into relational database nodes (Questions and Choices) 
    via regex and string manipulation to rapidly build large question banks.
    """
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    if request.method == 'POST':
        # --- NEW: FAST PASTE TEXT PARSER ---
        if 'raw_questions_text' in request.POST:
            raw_text = request.POST.get('raw_questions_text', '')
            if raw_text:
                try:
                    lines = raw_text.strip().split('\n')
                    current_section = "General"
                    current_question = None
                    current_marks = 1
                    choices = []
                    questions_created = 0
                    
                    import re
                    
                    for line in lines:
                        line = line.strip()
                        if not line: continue # Skip empty lines
                        
                        # Parse section headers (e.g., [SECTION: Aptitude])
                        if line.upper().startswith('[SECTION:') or line.upper().startswith('SECTION:'):
                            current_section = line.split(':', 1)[1].strip().strip(']')
                            continue
                            
                        # Parse MARKS lines (e.g., MARKS: 2)
                        if line.upper().startswith('MARKS:'):
                            try:
                                current_marks = int(line.split(':', 1)[1].strip())
                            except ValueError:
                                pass
                            continue
                            
                        # Parse ANSWER lines (e.g., ANSWER: C)
                        if line.upper().startswith('ANSWER:'):
                            ans_letter = line.split(':', 1)[1].strip().upper()
                            correct_idx = ord(ans_letter) - 65 # Convert A->0, B->1, etc.
                            
                            # Save the question since we've reached the end of its block
                            if current_question and choices:
                                q_obj = Question.objects.create(
                                    exam=exam, text=current_question, 
                                    section_name=current_section, marks=current_marks
                                )
                                for i, c_text in enumerate(choices):
                                    Choice.objects.create(
                                        question=q_obj, text=c_text, is_correct=(i == correct_idx)
                                    )
                                questions_created += 1
                                current_question = None
                                choices = []
                                current_marks = 1  # Reset marks for next question
                            continue
                            
                        # Parse Choice lines (e.g., A. Choice Text or B) Choice Text)
                        match = re.match(r'^([A-D])[\.\)]\s*(.*)', line, re.IGNORECASE)
                        if match:
                            choices.append(match.group(2).strip())
                        else:
                            # Parse Question Text
                            if current_question is None:
                                current_question = line
                            else:
                                current_question += "\n" + line
                                
                    messages.success(request, f"{questions_created} questions added instantly via Fast Paste!")
                    return redirect('exam_detail', pk=exam.pk)
                except Exception as e:
                    messages.error(request, f"Error parsing text format: {str(e)}")
                    
        # --- EXISTING: JSON BUILDER PARSER ---
        else:
            try:
                questions_data = json.loads(request.POST.get('questions_json', '[]'))
                for q_data in questions_data:
                    question = Question.objects.create(
                        exam=exam,
                        text=q_data.get('text'),
                        section_name=q_data.get('section_name', 'General'),
                        marks=int(q_data.get('marks', 1))
                    )
                    choices = q_data.get('choices', [])
                    for idx, choice_text in enumerate(choices, start=1):
                        # Validate against whichever index the user selected as correct
                        is_correct = (str(idx) == str(q_data.get('correct_choice')))
                        if choice_text:
                            Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
                
                messages.success(request, f"{len(questions_data)} questions successfully imported!")
                return redirect('exam_detail', pk=exam.pk)
            except Exception as e:
                messages.error(request, f"Error processing bulk import: {str(e)}")
            
    return render(request, 'exams/bulk_add_questions.html', {'exam': exam})

@login_required
def delete_question(request, pk):
    """
    Teacher deletes a specific question from an exam.
    """
    question = get_object_or_404(Question, pk=pk, exam__teacher=request.user)
    if request.method == 'POST':
        exam_id = question.exam.id
        question.delete()
        messages.success(request, "Question deleted successfully.")
        return redirect('exam_detail', pk=exam_id)
    return redirect('home')

@login_required
def view_exam_results(request, pk):
    """
    Teacher views results for a specific exam they authored.
    """
    if not getattr(request.user, 'is_teacher', False):
        messages.error(request, "Access denied.")
        return redirect('home')
        
    exam = get_object_or_404(Exam, pk=pk, teacher=request.user)
    results = Result.objects.filter(exam=exam).order_by('-score', 'completed_at')
    
    return render(request, 'exams/view_results.html', {'exam': exam, 'results': results})

# --- STUDENT VIEWS ---

@login_required
def student_dashboard(request):
    """
    Renders the Student Interface mapped strictly out of the Examify ecosystem.
    Calculates and packages data including Available Exams (filtered dynamically
    by Department and Semester) and historical Academic Transcripts.
    Outputs comprehensive KPIs such as pass/fail ratios and colored score indications.
    """
    if not getattr(request.user, 'is_student', False):
        messages.error(request, "Access denied. Only students can view this page.")
        return redirect('home')
        
    # Get all exams the student hasn't taken yet
    taken_exam_ids = Result.objects.filter(student=request.user).values_list('exam_id', flat=True)
    available_exams = Exam.objects.exclude(id__in=taken_exam_ids)
    
    # Department Filtering: Ensure students only see exams intended for their department
    if getattr(request.user, 'department', None):
        from django.db.models import Q
        available_exams = available_exams.filter(
            Q(department=request.user.department) | Q(department__isnull=True)
        )
        
    student_courses = []
    if request.user.department and request.user.semester:
        student_courses = Course.objects.filter(department=request.user.department, semester=request.user.semester)
        
    selected_course_id = request.GET.get('course_id')
    if selected_course_id:
        available_exams = available_exams.filter(course_id=selected_course_id)
        
    past_results = Result.objects.filter(student=request.user).order_by('-completed_at')
    
    # MCA Level KPI Calculations
    total_attempted = past_results.count()
    passed_count = 0
    total_percentage_sum = 0
    
    enriched_results = []
    
    for res in past_results:
        # Determine Pass/Fail (threshold = 50%)
        passing_score = res.exam.total_marks / 2
        is_pass = res.score >= passing_score
        
        if is_pass:
            passed_count += 1
            
        # Determine Color Status
        percentage = (res.score / res.exam.total_marks) * 100 if res.exam.total_marks > 0 else 0
        total_percentage_sum += percentage
        
        color = 'black'
        if percentage >= 80:
            color = '#38a169'  # Green
        elif percentage < 50:
            color = '#e53e3e'  # Red
        else:
            color = '#d69e2e'  # Orange/Yellow
            
        # Attach dynamic fields safely onto the object for the template to digest
        res.is_pass = is_pass
        res.color = color
        res.percentage = percentage
        enriched_results.append(res)
        
    avg_score = round(total_percentage_sum / total_attempted, 2) if total_attempted > 0 else 0
    
    context = {
        'available_exams': available_exams,
        'past_results': enriched_results,
        'kpi_total_attempted': total_attempted,
        'kpi_passed_count': passed_count,
        'kpi_avg_score': avg_score,
        'student_courses': student_courses,
        'selected_course_id': int(selected_course_id) if selected_course_id else None
    }
    return render(request, 'exams/student_dashboard.html', context)

@login_required
def take_exam(request, pk):
    """
    Handles live interaction of taking an exam by the student object.
    Implements a strict single-submission policy per student per exam.
    On POST (submission), calculates scores including dynamic negative marking logic
    (deducts fractional/decimal amounts per incorrect answer instead of 0).
    Saves and generates the corresponding Result metric object asynchronously.
    """
    if not getattr(request.user, 'is_student', False):
        return redirect('home')
        
    exam = get_object_or_404(Exam, pk=pk)
    
    # Check if student already took it
    if Result.objects.filter(student=request.user, exam=exam).exists():
        messages.warning(request, "You have already taken this exam.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        score = 0
        exam_questions = exam.questions.all()
        # For each question, find what the student submitted
        for q in exam_questions:
            selected_choice_id = request.POST.get(f'question_{q.id}')
            if selected_choice_id:
                try:
                    choice = Choice.objects.get(id=selected_choice_id)
                    if choice.is_correct:
                        score += q.marks
                    elif exam.negative_marks > 0:
                        score -= exam.negative_marks
                except Choice.DoesNotExist:
                    pass
        
        # Prevent negative score since the Result field is PositiveIntegerField
        score = max(0, score)
                    
        # Save Result
        Result.objects.create(student=request.user, exam=exam, score=score)
        messages.success(request, f"Exam submitted! Your score is {score}/{exam.total_marks}")
        return redirect('student_dashboard')
        
    # GET request - prepare questions
    questions = list(exam.questions.all())
    if exam.shuffle_questions:
        random.shuffle(questions)
        
    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions})
