"""
accounts/admin.py
=================
This file registers our CustomUser model with the Django Admin panel.

By creating a custom ModelAdmin class (CustomUserAdmin), we can:
  - Control which fields appear in the user list table
  - Add search and filter capabilities
  - Organise the user edit form into logical sections
  - Display extra metadata (student_id, department, etc.)

Jazzmin will automatically style everything we register here with
its premium dark Bootstrap 4 UI.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Base class with password hashing built in
from django.utils.safestring import mark_safe    # Safely render HTML inside admin columns
from .models import CustomUser, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
# ===========================================================================
# CUSTOM USER ADMIN CLASS
# Extends Django's built-in UserAdmin so we keep all the password hashing,
# permission management, and group features — while adding our custom fields.
# ===========================================================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin controls how the CustomUser model is displayed
    and edited inside the Django admin panel.
    """

    # ------------------------------------------------------------------
    # LIST VIEW SETTINGS
    # These settings control the table that appears when you click
    # "Custom Users" in the admin sidebar — the list of all users.
    # ------------------------------------------------------------------

    # Columns shown in the list table (left to right)
    list_display = [
        'username',
        'email',
        'full_name_display',    # Custom method — shows combined first + last name
        'role_badge',           # Custom method — shows a coloured "Student"/"Teacher" badge
        'department',
        'student_id',
        'is_active',
        'date_joined',
    ]

    # Fields that trigger a search when you type in the search box
    search_fields = ['username', 'email', 'first_name', 'last_name', 'student_id']

    # Right-side filter panel options
    list_filter = [
        'is_student',       # Filter by role: show only students
        'is_teacher',       # Filter by role: show only teachers
        'department',       # Filter by department
        'year_of_study',    # Filter by year
        'is_active',        # Filter by active/inactive accounts
        'is_staff',         # Filter by staff (admin) status
        'date_joined',      # Filter by when the user registered
    ]

    # How many records per page in the list view
    list_per_page = 20

    # Make clicking the username open the edit form (default is the first column)
    list_display_links = ['username']

    # Fields that can be edited directly in the list view (inline editing)
    list_editable = ['is_active']

    # Default ordering: newest users appear first
    ordering = ['-date_joined']

    # ------------------------------------------------------------------
    # DETAIL / EDIT FORM SETTINGS
    # These fieldsets control the layout of the form when you click
    # on a user to edit them. Sections are grouped with headings.
    # ------------------------------------------------------------------
    fieldsets = (
        # Section 1: Core login credentials
        ('Login Credentials', {
            'fields': ('username', 'password'),
            'description': 'The username and password used to log into the system.'
        }),

        # Section 2: Personal identity information
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'email', 'profile_image'),
            'description': 'Full name details and contact email for this user.'
        }),

        # Section 3: Custom role flags — the most important section for our system
        ('Role & Access Control', {
            'fields': ('is_student', 'is_teacher'),
            'description': (
                '⚠️ IMPORTANT: Assign exactly one role. '
                'is_student=True → Student Portal. '
                'is_teacher=True → Teacher Portal.'
            ),
            # 'classes': ('collapse',),  # Uncomment to make this section collapsible
        }),

        # Section 4: Academic profile fields specific to students
        ('Academic Profile (Student Fields)', {
            'fields': ('student_id', 'department', 'year_of_study', 'semester'),
            'description': 'These fields apply to Student accounts only.',
            'classes': ('collapse',),  # Collapse by default to keep the form clean
        }),
        
        # Section: Teacher specific fields
        ('Teacher Profile Fields', {
            'fields': ('subjects',),
            'description': 'These fields apply to Teacher accounts only.',
            'classes': ('collapse',),
        }),

        # Section 5: Django system permissions (inherited from UserAdmin)
        ('System Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'Control this user\'s system-level access and Django group memberships.',
            'classes': ('collapse',),  # Collapse by default for cleaner UI
        }),

        # Section 6: Audit timestamps (read-only, set automatically by Django)
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'description': 'Automatically recorded timestamps. These cannot be edited manually.',
        }),
    )

    # ------------------------------------------------------------------
    # ADD USER FORM SETTINGS
    # This controls the fields shown when creating a NEW user from scratch
    # (different from the edit form above).
    # ------------------------------------------------------------------
    add_fieldsets = (
        # Basic credentials for the new account
        ('Create New Account', {
            'classes': ('wide',),  # 'wide' makes this section use more horizontal space
            'fields': ('username', 'email', 'password1', 'password2'),
            'description': 'Enter a username and set a password for the new user.'
        }),

        # Personal details
        ('Personal Details', {
            'classes': ('wide',),
            'fields': ('first_name', 'middle_name', 'last_name'),
        }),

        # Role assignment — critical for determining which portal the user accesses
        ('Assign Role', {
            'classes': ('wide',),
            'fields': ('is_student', 'is_teacher'),
            'description': 'Select exactly one role for this user.',
        }),

        # Student-specific academic fields
        ('Academic Details (for Students)', {
            'classes': ('wide',),
            'fields': ('student_id', 'department', 'year_of_study', 'semester'),
        }),
        
        ('Teacher Details', {
            'classes': ('wide',),
            'fields': ('subjects',),
        }),
    )

    # Make certain timestamp fields read-only (they're auto-set by Django)
    readonly_fields = ('date_joined', 'last_login')

    # ------------------------------------------------------------------
    # CUSTOM DISPLAY METHODS
    # These are methods called by list_display to render custom columns.
    # ------------------------------------------------------------------

    def full_name_display(self, obj):
        """
        Returns the user's full name (first + middle + last).
        Falls back to their username if no name is set.
        Used as a custom column in the list view.
        """
        # filter(None, ...) removes empty/None values cleanly
        parts = filter(None, [obj.first_name, obj.middle_name, obj.last_name])
        full = ' '.join(parts)
        return full if full else obj.username

    # Column header text in the admin list table
    full_name_display.short_description = 'Full Name'

    def role_badge(self, obj):
        """
        Returns a colour-coded HTML badge showing the user's role.
        - Green  → Student
        - Blue   → Teacher
        - Red    → Superuser (Admin)
        - Grey   → No role assigned yet

        format_html() is used to safely inject HTML without XSS risks.
        """
        if obj.is_superuser:
            # Red badge for superadmin accounts
            return mark_safe(
                '<span style="background:#e53e3e; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">🔑 Admin</span>'
            )
        elif obj.is_teacher:
            # Blue badge for teacher accounts
            return mark_safe(
                '<span style="background:#3182ce; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">🎓 Teacher</span>'
            )
        elif obj.is_student:
            # Green badge for student accounts
            return mark_safe(
                '<span style="background:#38a169; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">📚 Student</span>'
            )
        else:
            # Grey badge — no role means the user can't access any portal
            return mark_safe(
                '<span style="background:#718096; color:white; padding:3px 10px; '
                'border-radius:12px; font-size:0.8rem; font-weight:bold;">— No Role</span>'
            )

    role_badge.short_description = 'Role'
    # Tells Django this column produces HTML (needed for coloured badges)
    role_badge.allow_tags = True
