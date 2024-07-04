from django import forms
from .models import Task
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'due_date','status']

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.now().date():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=Task.STATUS_CHOICES) 
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
