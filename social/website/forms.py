from django import forms

class UserForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30)
    firstName = forms.CharField(label="First name", max_length=30)
    lastName = forms.CharField(label="Last name", max_length=30)
    password = forms.CharField(label="Password", max_length=30, min_length=8)
    password = forms.CharField(label="Repeat password", max_length=30, min_length=8)