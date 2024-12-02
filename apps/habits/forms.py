from django import forms
from .models import Habit

class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password' )

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8)

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            "name",
            "frequency",
        ]

        # widgets = {
        #     'name': forms.WidgetType(attrs)
        # }