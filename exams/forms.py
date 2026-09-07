from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'course', 'title', 'total_marks', 'duration_minutes', 
            'scheduled_date', 'negative_marks', 'shuffle_questions', 'instructions'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit Test 1 - Data Structures'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '60'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'negative_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.0 for none'}),
            'shuffle_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter instructions for students to read before starting the exam here...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExamForm, self).__init__(*args, **kwargs)
        
        if self.user:
            self.fields['course'].queryset = self.user.subjects.all()
                
        # Strip help text
        self.fields['title'].help_text = None
        self.fields['total_marks'].help_text = None
        self.fields['duration_minutes'].help_text = None
        self.fields['scheduled_date'].help_text = None
