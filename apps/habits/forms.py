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

class CompletedForm(forms.Form):
    habit_id = forms.IntegerField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.HiddenInput())
    # TODO: notes = forms.CharField(required=False)
    # TODO: Add custom scale for completion - eg. do 100 pushups, etc

class UncompletedForm(forms.Form):
    pass