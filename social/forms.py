from social.models import *
from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Message'}))