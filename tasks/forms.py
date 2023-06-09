from django import forms
from .models import Task, Snippet

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','descripcion','important']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'title'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'description'}),
            'important':forms.CheckboxInput(attrs={'class':'form-check-input text-center'})
        }


# class SnippetForm(forms.ModelForm):
#     class Meta:
#         model = Snippet
#         fields = ['title','descripcion','important']
#         widgets = {
#             'title':forms.TextInput(attrs={'class':'form-control','placeholder':'title'}),
#             'description':forms.Textarea(attrs={'class':'form-control','placeholder':'description'})
#         }