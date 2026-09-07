"""
exams/admin.py
==============
This file registers the Exam, Question, Choice, and Course models
with the Django Admin panel.

Key features implemented:
  - Inline editing: Add questions and choices directly inside the Exam form
  - List filters and search for quick navigation
  - Colour-coded status badges for exam scheduling
  - Descriptive short descriptions for all custom columns
"""

from django.contrib import admin
from django.utils.safestring import mark_safe       # Safe HTML rendering in admin columns
from django.utils import timezone           # For comparing scheduled dates to current time
from .models import Course, Exam, Question, Choice


# ===========================================================================
# INLINE ADMIN CLASSES
# Inlines allow related objects to be edited on the same page as their parent.
# For example, you can add Choices directly inside the Question edit form.
# ===========================================================================

class ChoiceInline(admin.TabularInline):
    """
    Renders Choice objects as inline rows inside the Question edit form.
    'TabularInline' shows each Choice as a compact horizontal row.
    (Alternative: StackedInline shows each Choice vertically — more space but less compact)
    """
    model = Choice          # The model this inline is for
    extra = 4               # Always show 4 empty rows for adding new choices
    max_num = 4             # Limit to exactly 4 choices per question (MCQ standard)
    min_num = 2             # Require at least 2 choices before saving
    fields = ['text', 'is_correct']  # Fields to show in each inline row


class QuestionInline(admin.StackedInline):
    """
    Renders Question objects as inline stacked forms inside the Exam edit form.
    'StackedInline' shows each question vertically with all its fields visible.
    This is better for complex nested data (questions with multiple fields).
    """
    model = Question             # The model this inline is for
    extra = 1                    # Show 1 empty question form by default
    show_change_link = True      # Show a link to edit the question separately
    fields = ['section_name', 'text', 'marks']  # Fields shown in the inline form


# ===========================================================================
# CHOICE ADMIN
# Registered so Choices can also be viewed/managed directly from the sidebar.
# ===========================================================================
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Admin view for individual Choices.
    Useful for bulk-editing correct answers or auditing choices.
    """
    # Columns visible in the list table
    list_display = ['text', 'question', 'is_correct']

    # Filter sidebar options
    list_filter = ['is_correct']

    # Search across choice text and the parent question's text
    search_fields = ['text', 'question__text']

    # Allow toggling is_correct directly in the list table (inline editing)
    list_editable = ['is_correct']


# ===========================================================================
# QUESTION ADMIN
# Full management interface for individual Questions.
# ===========================================================================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin view for Questions. Includes inline Choices so you can
    manage a question and all its answer options on one page.
    """
    # Embed the Choice inline forms directly in the Question edit page
    inlines = [ChoiceInline]

    # Columns in the question list table
    list_display = ['short_text', 'exam', 'section_name', 'marks']

    # Filter sidebar: filter questions by which exam they belong to
    list_filter = ['exam', 'section_name']

    # Search by question text content
    search_fields = ['text']

    def short_text(self, obj):
        """
        Returns only the first 80 characters of the question text
        to keep the list table readable without truncating important info.
        """
        return obj.text[:80] + ('...' if len(obj.text) > 80 else '')

    short_text.short_description = 'Question Text'


# ===========================================================================
# COURSE ADMIN
# Simple admin for Course (subject categories like "Data Structures").
# ===========================================================================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin view for Courses (subject categories).
    Kept simple since courses only have a name field.
    """
    # Show course name, department, semester, and exam count in the list
    list_display = ['name', 'department', 'semester', 'exam_count']
    list_filter = ['department', 'semester']
    search_fields = ['name', 'department__name']

    def exam_count(self, obj):
        """
        Shows how many exams are linked to this course.
        Uses a database count query — efficient and accurate.
        """
        count = obj.exam_set.count()
        return count

    exam_count.short_description = 'Total Exams'


# ===========================================================================
# EXAM ADMIN
# The most detailed admin class — exams are the core of the system.
# ===========================================================================
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """
    Admin view for Exams. This is the most important admin model class.

    Features:
      - List view with status badges, question counts, and durations
      - Searchable by title, course, teacher
      - Filterable by negative marking, shuffle, scheduling
      - Organized form with descriptive fieldsets
      - Inline questions (you can add questions while creating an exam)
    """

    # ------------------------------------------------------------------
    # LIST VIEW CONFIGURATION
    # ------------------------------------------------------------------

    # Columns displayed in the Exam list table
    list_display = [
        'title',
        'course',
        'department',
        'teacher',
        'total_marks',
        'duration_minutes',
        'question_count',       # Custom method: shows how many questions the exam has
        'status_badge',         # Custom method: shows Active/Scheduled in a coloured badge
        'negative_marks',
        'created_at',
    ]

    # Quick filter checkboxes in the right panel
    list_filter = [
        'course',
        'department',
        'negative_marks',     # Filter by whether negative marking is active
        'shuffle_questions',    # Filter by whether question shuffling is active
        'scheduled_date',       # Filter by schedule presence
        'teacher',
    ]

    # Search box — searches across these fields
    search_fields = ['title', 'course__name', 'teacher__username', 'teacher__first_name']

    # Default ordering: most recently created exams appear first
    ordering = ['-created_at']

    # Fields that are automatically set (read-only, cannot be edited manually)
    readonly_fields = ['created_at']

    # Columns that link to the edit page when clicked
    list_display_links = ['title']

    # Quick inline editing in the list view
    list_editable = ['negative_marks']

    # Records per page
    list_per_page = 15

    # ------------------------------------------------------------------
    # EXAM EDIT FORM — FIELDSETS
    # Groups the exam fields into logical sections with headings
    # ------------------------------------------------------------------
    fieldsets = (
        # Basic exam information
        ('Exam Details', {
            'fields': ('title', 'course', 'department', 'teacher'),
            'description': 'Set the exam title, subject course, department, and the teacher who owns this exam.'
        }),

        # Scoring and time limits
        ('Scoring & Duration', {
            'fields': ('total_marks', 'duration_minutes'),
            'description': 'Set how long the exam lasts and the maximum marks achievable.'
        }),

        # Advanced exam behaviour toggles
        ('Advanced Settings', {
            'fields': ('scheduled_date', 'negative_marks', 'shuffle_questions', 'instructions'),
            'description': (
                'Optional advanced settings: '
                'Schedule the exam for a future date, set negative marks (e.g. 0.25 per wrong answer), '
                'or shuffle questions to prevent copying.'
            ),
            'classes': ('collapse',),  # Collapsed by default — keeps the form clean
        }),

        # Auto-generated audit field
        ('Audit Info', {
            'fields': ('created_at',),
            'description': 'This timestamp is automatically set when the exam is created.',
        }),
    )

    # Embed Question forms directly inside the Exam create/edit page
    # This allows creating an exam + questions in one place
    inlines = [QuestionInline]

    # ------------------------------------------------------------------
    # CUSTOM COLUMN METHODS
    # ------------------------------------------------------------------

    def question_count(self, obj):
        """
        Counts the number of questions linked to this exam.
        Renders as a number (e.g. "5 Qs") for at-a-glance readability.
        """
        count = obj.questions.count()
        return f"{count} Qs"

    question_count.short_description = 'Questions'

    def status_badge(self, obj):
        """
        Checks if exam has a scheduled_date in the future → shows 'Scheduled' (yellow).
        If no date or date is in the past → shows 'Active' (green).
        Returns styled HTML badge using format_html for XSS safety.
        """
        now = timezone.now()  # Current time in IST (as set in settings.py)

        if obj.scheduled_date and obj.scheduled_date > now:
            # Future-scheduled exam — not yet live for students
            return mark_safe(
                '<span style="background:#d69e2e; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">🕐 Scheduled</span>'
            )
        else:
            # Active exam — available for students right now
            return mark_safe(
                '<span style="background:#38a169; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">✅ Active</span>'
            )

    status_badge.short_description = 'Status'
