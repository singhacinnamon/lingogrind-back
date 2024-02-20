from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField(max_length=150)
    password = forms.CharField(min_length=8)