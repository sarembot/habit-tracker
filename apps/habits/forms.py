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

class HabitForm(forms.ModelForm): #ModelForm automatically creates fields based on the model
    frequency = forms.ChoiceField(
        choices=Habit.FREQUENCY_CHOICES,
        widget=forms.RadioSelect, # instead of default dropdown
        initial='daily'
    )
    class Meta:
        model = Habit
        fields = [
            "name",
            "frequency",
        ]

        # widgets = {
        #     'name': forms.WidgetType(attrs)
        # }