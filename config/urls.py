"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect, render

def dynamic_home(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'is_student', False):
            return redirect('student_dashboard')
        if getattr(request.user, 'is_teacher', False):
            return redirect('teacher_dashboard')
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts app URLs for login, register, etc.
    path('accounts/', include('accounts.urls')),
    # Exams app URLs
    path('exams/', include('exams.urls')),
    # Home page dashboard
    path('', dynamic_home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
