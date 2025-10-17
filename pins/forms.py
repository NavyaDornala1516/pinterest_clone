from django import forms
from .models import Board, Pin

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description', 'is_private']

class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['board', 'title', 'image', 'description']
