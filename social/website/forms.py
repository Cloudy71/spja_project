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
    type = forms.IntegerField(min_value=-1, max_value=1)


class FollowForm(forms.Form):
    user = forms.CharField()
    type = forms.IntegerField()


class ResponseForm(forms.Form):
    main_post = forms.IntegerField()
    content = forms.CharField(min_length=1)


class VisibilityForm(forms.Form):
    post = forms.IntegerField()
    visibility = forms.IntegerField(min_value=0, max_value=2)

class ChangePassword(forms.Form):
    old_password = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Old password")
    new_password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput, label="New password")
    new_password = forms.CharField(min_length=8, widget=forms.PasswordInput, label="Repeat new password")

class ChangeName(forms.Form):
    new_name = forms.CharField(min_length=1, label="Name")
    new_surname = forms.CharField(min_length=1, label="Surname")
