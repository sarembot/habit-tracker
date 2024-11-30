from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

# request param contains all the info about the current HTTP request


def home(request):
    return render(request, 'habits/home.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # user is found and password matches
                auth_login(request, user) # create a session
                return redirect('home')
            else: 
                # authentication failed
                form.add_error(None, "Invalid username or password")

    else:
        form = LoginForm()
    return render(request, 'habits/registration/login.html', {'form' : form})

def signup(request):
    if request.method == 'POST': # handle form submission
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
    else: # display empty form
        form = SignUpForm() 
    return render(request, 'habits/registration/signup.html', {'form': form})

def success(request):
    return render(request, 'habits/registration/success.html')

def habits(request):
    return render(request, 'habits/habits.html')