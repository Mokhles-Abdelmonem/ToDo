from django import forms
from .models import *




class AddTaskForm(forms.ModelForm):
    group_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "task",
                "class": "w3-input w3-border w3-sand",
                "name":"first",
            }
        ))
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "task",
                "class": "w3-input w3-border w3-sand",
                "name":"first",
            }
        ))

    
    class Meta:
        model = Task
        fields = ('text',)

