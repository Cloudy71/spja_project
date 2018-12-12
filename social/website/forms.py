from django import forms


class UserForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, min_length=4)
    firstName = forms.CharField(label="First name", max_length=30)
    lastName = forms.CharField(label="Last name", max_length=30)
    password = forms.CharField(label="Password", max_length=30, min_length=8, widget=forms.PasswordInput)
    repeated_password = forms.CharField(label="Repeat password", max_length=30, min_length=8,
                                        widget=forms.PasswordInput)
    email = forms.EmailField(label="Email address")


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, min_length=4)
    password = forms.CharField(label="Password", max_length=30, min_length=8, widget=forms.PasswordInput)


class Post(forms.Form):
    text = forms.CharField(widget=forms.Textarea, min_length=1)


class ThumbForm(forms.Form):
    post = forms.IntegerField()
    type = forms.IntegerField()


class FollowForm(forms.Form):
    user = forms.CharField()
    type = forms.IntegerField()
