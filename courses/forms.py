from django import forms

class EnrollForm(forms.Form):
    access_key = forms.CharField(widget=forms.PasswordInput)