from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['company', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, SQL'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us why you are the perfect fit...'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'company_notes']
        widgets = {
            'company_notes': forms.Textarea(attrs={'rows': 3}),
        }
