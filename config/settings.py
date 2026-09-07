"""
Django Settings for the Examify Online Examination Management System.

This file controls the entire configuration of the Django application:
  - Database connections
  - Installed apps (including third-party packages like Jazzmin)
  - Authentication settings
  - Static & media file paths
  - Admin panel branding (via Jazzmin)
"""

from pathlib import Path

# -------------------------------------------------------------------
# BASE DIRECTORY
# Path(__file__) gives us the absolute path to this settings.py file.
# .resolve().parent.parent gives us the project root (Examify/).
# All other paths are built relative to this.
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------------------------
# SECURITY SETTINGS
# WARNING: Keep SECRET_KEY secret in production. Never commit it to GitHub.
# DEBUG=True shows detailed error pages. Set to False in production.
# -------------------------------------------------------------------
SECRET_KEY = 'django-insecure-lngntpfjg)dcl!50l-ho)!c#@^$-8ioa4b0f9$4mq2$=p8&_sb'
DEBUG = False
ALLOWED_HOSTS = ['sarim2255.pythonanywhere.com', 'www.sarim2255.pythonanywhere.com', '*']


# -------------------------------------------------------------------
# JAZZMIN ADMIN PANEL CONFIGURATION
# Jazzmin is a third-party package that replaces Django's default admin UI
# with a sleek, modern Bootstrap 4 interface. All customization is done here.
# -------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    # The text shown at the top of the browser tab and in the sidebar header
    "site_title": "Examify Admin",

    # The large brand name in the top-left corner of the admin sidebar
    "site_header": "Examify",

    # The brand name shown on the login page of the admin panel
    "site_brand": "Examify Portal",

    # Welcome text shown below the login form on the admin login page
    "welcome_sign": "Welcome to Examify Admin Panel",

    # Copyright text in the footer of every admin page
    "copyright": "Examify — Mohd Sarim Khan © 2026",

    # The SVG icon for the site (uses Font Awesome class names)
    # "fas fa-graduation-cap" renders a graduation cap icon ► suitable for an exam platform
    "site_icon": None,
    "site_logo": None,          # Path to a logo image (optional, None = text only)
    "site_logo_classes": "img-circle",  # CSS class for logo image

    # Top navigation bar links (appear across the top of the admin panel)
    "topmenu_links": [
        # Link to the main site homepage — opens in the same tab
        {"name": "🏠 View Main Site", "url": "/", "new_window": False},

        # Quick link to the Exams list for fast management
        {"model": "exams.exam"},

        # Quick link to the CustomUser list for user management
        {"model": "accounts.customuser"},
    ],

    # Sidebar user profile menu links (shown when clicking the logged-in username)
    "usermenu_links": [
        # Link back to the main Examify site
        {"name": "🌐 Main Site", "url": "/", "new_window": False},
    ],

    # ------------------------------------------------------------------
    # SIDEBAR NAVIGATION CONFIGURATION
    # This controls what appears in the left sidebar nav.
    # You can group models by app or create custom menus.
    # ------------------------------------------------------------------
    "show_sidebar": True,       # Always keep the sidebar visible
    "navigation_expanded": True, # Expand all sections by default (no clicking needed to see items)
    "hide_apps": [],            # Apps to completely hide from sidebar (none hidden here)
    "hide_models": [],          # Individual models to hide

    # Custom sidebar order — controls the order of app groups in the sidebar
    "order_with_respect_to": [
        "accounts",     # User management appears first
        "exams",        # Exams section second
        "results",      # Results section third
        "auth",         # Django's built-in auth (groups, permissions) last
    ],

    # ------------------------------------------------------------------
    # UI/THEME CUSTOMIZATION
    # These settings control the visual appearance of the admin panel.
    # ------------------------------------------------------------------

    # Bootstrap theme skin color for the admin sidebar and top bar
    # We use "lumen" for a sleek, clean, bright professional look
    "theme": "lumen",

    # Disable dark mode theme completely
    "dark_mode_theme": None,

    # Color of the top navigation bar
    "navbar_color": "white",

    # Whether to show bookmarks in the sidebar header (admin can save quick links)
    "show_ui_builder": False,   # Hide the Jazzmin UI builder button (clean UI)

    # ------------------------------------------------------------------
    # ICONS FOR MODELS IN THE SIDEBAR
    # Uses Font Awesome Free icon class names (fas = solid, far = regular, fab = brand)
    # Format: "app_name.ModelName": "fas fa-icon-name"
    # ------------------------------------------------------------------
    "icons": {
        # Auth app icons
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",

        # Accounts app icons
        "accounts": "fas fa-id-card",
        "accounts.CustomUser": "fas fa-user-graduate",

        # Exams app icons
        "exams": "fas fa-file-alt",
        "exams.Course": "fas fa-book",
        "exams.Exam": "fas fa-pen-square",
        "exams.Question": "fas fa-question-circle",
        "exams.Choice": "fas fa-check-square",

        # Results app icons
        "results": "fas fa-chart-bar",
        "results.Result": "fas fa-trophy",
    },

    # Use these icons as default for any model not explicitly listed above
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",

    # ------------------------------------------------------------------
    # RELATED MODAL POPUPS
    # When clicking a ForeignKey field in a form, use a popup rather than
    # redirection — delivers a better user experience
    # ------------------------------------------------------------------
    "related_modal_active": True,

    # ------------------------------------------------------------------
    # TABLE SETTINGS
    # Controls the appearance of model list views (the data tables)
    # ------------------------------------------------------------------
    "changeform_format": "horizontal_tabs",  # Show model form sections as horizontal tabs

    # Custom CSS/JS (relative to your static files)
    "custom_css": None,
    "custom_js": None,

    # Whether to show the "object tools" (Save buttons) at top of form page as well
    "show_ui_builder": False,
}

# -------------------------------------------------------------------
# JAZZMIN UI SETTINGS (separate from main settings above)
# These control fine-grained Bootstrap and layout behaviors.
# -------------------------------------------------------------------
JAZZMIN_UI_TWEAKS = {
    # Navbar variant — "light" or "dark" (affects nav link text color)
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    # Sidebar appearance
    "brand_colour": "navbar-white",          # Brand text color on sidebar
    "accent": "accent-primary",              # Accent color for hovered sidebar links
    "navbar": "navbar-white navbar-light",   # Navbar style (white bg, dark text)
    "no_navbar_border": False,               # Add border
    "navbar_fixed": True,                    
    "layout_boxed": False,                   
    "footer_fixed": False,                   
    "sidebar_fixed": True,                   
    "sidebar": "sidebar-light-primary",      # Sidebar color — light with primary accents
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,         
    "sidebar_nav_child_indent": True,        
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,

    # Theme controls
    "theme": "lumen",
    "dark_mode_theme": None,

    # UI buttons and actions
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# -------------------------------------------------------------------
# INSTALLED APPLICATIONS
# Django loads these in order. 'jazzmin' MUST come before 'django.contrib.admin'
# so it can override the default admin templates.
# -------------------------------------------------------------------
INSTALLED_APPS = [
    # ← Jazzmin MUST be first before django.contrib.admin to override admin templates
    'jazzmin',

    # Core Django apps (authentication, admin, sessions, etc.)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our custom Examify apps
    'accounts',     # Handles user authentication, registration, and user profiles
    'exams',        # Handles exam creation, question management, and exam logic
    'results',      # Handles storing and displaying student exam results
]

# -------------------------------------------------------------------
# CUSTOM USER MODEL
# We override Django's default User model with our own CustomUser
# which adds fields like is_student, is_teacher, department, etc.
# -------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.CustomUser'

# -------------------------------------------------------------------
# MIDDLEWARE STACK
# Middleware is code that runs on every HTTP request/response cycle.
# Order matters here — each middleware wraps the one below it.
# -------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # Enforces HTTPS and other security headers
    'whitenoise.middleware.WhiteNoiseMiddleware',            # Serves static files magically
    'django.contrib.sessions.middleware.SessionMiddleware',  # Handles user session management (cookies)
    'django.middleware.common.CommonMiddleware',             # Handles URL trailing slashes and content types
    'django.middleware.csrf.CsrfViewMiddleware',             # Protects forms from Cross-Site Request Forgery attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Attaches the authenticated user to every request
    'django.contrib.messages.middleware.MessageMiddleware',  # Enables flash messages (success/error notifications)
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Prevents the site from being embedded in iframes
]

# -------------------------------------------------------------------
# URL CONFIGURATION
# This points Django to the main urls.py file that maps URLs to views.
# -------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# -------------------------------------------------------------------
# TEMPLATE CONFIGURATION
# Tells Django how to find and render HTML templates.
# - DIRS: extra directories to search (our project-level templates/ folder)
# - APP_DIRS: also search each app's templates/ folder automatically
# -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # Project-wide templates directory
        'APP_DIRS': True,                    # Also checks each app's own templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',   # Makes 'request' available in templates
                'django.contrib.auth.context_processors.auth',  # Makes 'user' and 'perms' available in templates
                'django.contrib.messages.context_processors.messages', # Makes 'messages' available in templates
            ],
        },
    },
]

# -------------------------------------------------------------------
# WSGI APPLICATION
# The entry point for WSGI-compatible web servers (like Gunicorn).
# -------------------------------------------------------------------
WSGI_APPLICATION = 'config.wsgi.application'

# -------------------------------------------------------------------
# DATABASE CONFIGURATION
# SQLite is used here for development simplicity.
# For production, switch to PostgreSQL or MySQL.
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',    # Database engine
        'NAME': BASE_DIR / 'db.sqlite3',           # Path to the database file
    }
}

# -------------------------------------------------------------------
# PASSWORD VALIDATION RULES
# Django runs these validators when a user sets/changes their password.
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    # Prevents passwords too similar to the username or email
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Minimum password length (default: 8 characters)
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # Blocks common/weak passwords like "password123"
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Blocks passwords that are entirely numeric (easy to brute-force)
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# INTERNATIONALIZATION & TIMEZONE
# -------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'      # Default language for the site
TIME_ZONE = 'Asia/Kolkata'   # IST timezone for Indian users (UTC+5:30)
USE_I18N = True              # Enable Django's internationalization framework
USE_TZ = True                # Store datetimes in the database as UTC, display in TIME_ZONE

# -------------------------------------------------------------------
# STATIC FILES (CSS, JavaScript, Fonts, Images)
# Static files are assets that don't change per-user.
# For development, Django serves these automatically when DEBUG=True.
# -------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# -------------------------------------------------------------------
# AUTHENTICATION REDIRECTS
# These URLs are used after login and logout actions.
# -------------------------------------------------------------------
LOGIN_REDIRECT_URL = 'home'    # After successful login, go to the home view
LOGOUT_REDIRECT_URL = 'home'   # After logging out, go back to the home page

# -------------------------------------------------------------------
# EMAIL BACKEND (Development)
# Instead of actually sending emails, print them to the console.
# This is used for password reset emails during development.
# Set to a real SMTP backend in production.
# -------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# -------------------------------------------------------------------
# MEDIA FILES (User-Uploaded Content)
# MEDIA_URL: The URL prefix to access uploaded files in the browser
# MEDIA_ROOT: The filesystem directory where Django saves uploaded files
# -------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------------------------------------------
# DEFAULT AUTO FIELD
# Django uses this as the default primary key type for new models.
# BigAutoField uses 64-bit integers, suitable for large datasets.
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
