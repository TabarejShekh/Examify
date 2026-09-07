from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Department

class StudentRegistrationForm(UserCreationForm):
    """
    Form for registering a new student.
    """
    first_name = forms.CharField(max_length=30, required=True)
    middle_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    
    # Custom fields for student
    student_id = forms.CharField(max_length=20, required=True, help_text='Your University/College ID Number')
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    year_of_study = forms.ChoiceField(choices=CustomUser.YEAR_CHOICES, required=True)
    profile_image = forms.ImageField(required=False, help_text="Upload a professional profile picture")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Enforce exactly this order: first, middle, last
        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'student_id', 'department', 'year_of_study', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Simplify the messy Django password help text
        if 'password' in self.fields:
            self.fields['password'].help_text = "Your password must be at least 8 characters long."
        # Optional: simplify confirm password text if desired, but usually it's fine.

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.middle_name = self.cleaned_data.get('middle_name')
        user.department = self.cleaned_data.get('department')
        user.year_of_study = self.cleaned_data.get('year_of_study')
        user.profile_image = self.cleaned_data.get('profile_image')
        if commit:
            user.save()
        return user
