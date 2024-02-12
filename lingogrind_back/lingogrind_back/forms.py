from django import forms

class LoginForm(forms.Form):
    username = forms.Charfield(max_length=150)
    password = forms.Charfield(min_length=8)