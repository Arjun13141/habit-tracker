from django import forms
from .models import Habit, HabitCompletion

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Drink 8 glasses of water'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: Add details about this habit'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class HabitCompletionForm(forms.ModelForm):
    class Meta:
        model = HabitCompletion
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional: Add notes about today\'s completion'
            }),
        }