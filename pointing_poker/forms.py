from django import forms
from .models import Card


class VoteForm(forms.Form):
    card = forms.ModelChoiceField(queryset=Card.objects.all())
    user_name = forms.CharField(max_length=200)
    user_email = forms.EmailField()


class JoinGameForm(forms.Form):
    name = forms.CharField(max_length=200)
    # email = forms.EmailField()
