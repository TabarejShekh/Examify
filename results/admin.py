"""
results/admin.py
================
Registers the Result model with the Django admin panel.

Provides an organized view of all student exam results with:
  - Score display with colour-coded percentage badges
  - Pass/Fail status in the list
  - Filterable by exam and date
  - Searchable by student or exam name
"""

from django.contrib import admin
from django.utils.html import format_html  # Safe HTML rendering in admin columns
from django.utils.safestring import mark_safe
from .models import Result


# ===========================================================================
# RESULT ADMIN
# ===========================================================================
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """
    Admin view for Result objects.

    A Result is created every time a student submits an exam.
    This view lets admins see all submissions, scores, and pass/fail statuses.
    """

    # ------------------------------------------------------------------
    # LIST VIEW CONFIGURATION
    # ------------------------------------------------------------------

    # Columns shown in the Result list table
    list_display = [
        'student',          # Who took the exam
        'exam',             # Which exam they took
        'score_display',    # Custom: shows "18 / 20" in coloured text
        'pass_fail_badge',  # Custom: shows green PASS or red FAIL badge
        'percentage',       # Custom: computed percentage
        'completed_at',     # When the exam was submitted
    ]

    # Right-panel filter options
    list_filter = [
        'exam',             # Filter by specific exam
        'exam__course',     # Filter by course (subject)
        'completed_at',     # Filter by date (today, this week, etc.)
    ]

    # Search by student username or exam title
    search_fields = [
        'student__username',
        'student__first_name',
        'student__last_name',
        'exam__title',
    ]

    # Default: most recent results appear first
    ordering = ['-completed_at']

    # Make completed_at read-only (it's set automatically by auto_now_add)
    readonly_fields = ['completed_at']

    # Results per page
    list_per_page = 25

    # ------------------------------------------------------------------
    # CUSTOM COLUMN METHODS
    # ------------------------------------------------------------------

    def score_display(self, obj):
        """
        Shows the score as "X / Y" where X = raw score and Y = total marks.
        Colour-coded for readability:
          - Green  (≥80%) → Excellent performance
          - Orange (50–79%) → Passing performance
          - Red    (<50%)  → Failing grade
        """
        total = obj.exam.total_marks
        score = obj.score

        # Compute percentage safely (avoid division by zero)
        pct = (score / total * 100) if total > 0 else 0

        # Choose color based on percentage
        if pct >= 80:
            color = '#38a169'   # Green
        elif pct >= 50:
            color = '#d69e2e'   # Orange/Amber
        else:
            color = '#e53e3e'   # Red

        # Render the score as bold colored text
        return format_html(
            '<strong style="color:{};">{} / {}</strong>',
            color, score, total
        )

    score_display.short_description = 'Score'

    def pass_fail_badge(self, obj):
        """
        Returns a coloured PASS/FAIL badge based on whether the student
        scored at least 50% of the total marks (the passing threshold).
        """
        total = obj.exam.total_marks
        passing_score = total / 2   # 50% threshold

        if obj.score >= passing_score:
            return mark_safe(
                '<span style="background:#38a169; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">✅ PASS</span>'
            )
        else:
            return mark_safe(
                '<span style="background:#e53e3e; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">❌ FAIL</span>'
            )

    pass_fail_badge.short_description = 'Result'

    def percentage(self, obj):
        """
        Computes and returns the percentage score as a rounded string, e.g. "85.0%".
        """
        total = obj.exam.total_marks
        if total > 0:
            pct = round((obj.score / total) * 100, 1)
            return f"{pct}%"
        return "N/A"

    percentage.short_description = 'Percentage'
