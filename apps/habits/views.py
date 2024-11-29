from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User

# simple view that renders a template
def home(request):
    return render(request, 'habits/home.html')

def login(request):
    return render(request, 'habits/registration/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create new user
            user = User.objects.create_user(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password1"],
                )
            user.save() # Add user to db
            return redirect('success') # signup successful
        else:
            print(form.errors)
    else:
        form = SignUpForm() 
    return render(request, 'habits/registration/signup.html', {'form': form})

def success(request):
    return render(request, 'habits/registration/success.html')

def habits(request):
    return render(request, 'habits/habits.html')