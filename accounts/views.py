from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import StudentRegistrationForm

def register_student(request):
    """
    Student Registration View:
    This function intercepts HTTP Requests pointing to the Register URL.
    It manages the form processing for committing new entities to the CustomUser database table.
    """
    # If the user is submitting their credentials (submitting the form data)
    if request.method == 'POST':
        # Load the POST data and any uploaded files (like profile_image) into the form object
        form = StudentRegistrationForm(request.POST, request.FILES)
        
        # Django automatically validates character limits, password complexity, and email formats natively
        if form.is_valid():
            user = form.save()
            
            # Autonomously log the user in immediately after successful registration
            # to provide a frictionless UX (avoiding forcing them back to the login screen)
            login(request, user)
            
            # Flash success message onto the dashboard UI seamlessly 
            messages.success(request, f"Welcome {user.first_name}! Your account was created successfully.")
            return redirect('home')  # Routes to the dynamically allocated dashboard algorithm
    else:
        # If the user is simply requesting/viewing the page with a GET request, create an empty dictionary form
        form = StudentRegistrationForm()
        
    context = {'form': form}
    # Package the context dictionary and push it down into the HTML template to be dynamically rendered
    return render(request, 'accounts/register.html', context)
