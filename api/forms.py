from django import forms


class LoginModel(forms.Form):
    email = forms.EmailField(max_length=140)
    password = forms.PasswordInput()

# class formMoment(forms.Form):
#     xxx = forms.BooleanField()
