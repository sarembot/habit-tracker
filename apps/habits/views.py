from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, HabitForm, CompletedForm
from .models import Habit, User, CompletedHabit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

User = get_user_model()

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# request param contains all the info about the current HTTP request


def home(request):
    return render(request, 'habits/home.html')

# AUTHENTICATION ---------------------------------------
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

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('home')
    return render(request, 'habits/registration/logout.html')

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


# HABITS ---------------------------------------

@login_required
def habits(request):
    User = get_user_model()
    current_user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        habit_form = HabitForm(request.POST)
        if habit_form.is_valid():
            # Create new habit
            habit = habit_form.save(commit=False) # "pause" save 
            habit.user = current_user # associate user with habit
            habit.save() # complete save to db
            return redirect('habits')
    else:
        # Habits for dashboard table:
        habits = Habit.objects.filter(user=current_user) # find user's habits
        
        # Dates for dashboard table:
        today = datetime.today()
        dates = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i) 
            dates.append(date)
        dates.reverse()

        
        habit_form = HabitForm()

        # Context passed into template
        context = {
            'habits': habits,
            'dates': dates,
            'habit_form': habit_form,
        }


    return render(request, 'habits/habits.html', context)
    

# COMPLETED HABITS ---------------------------------

def completed(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        date = request.POST.get('date')

        # Search through instances of Habit to find the one with matching id
        habit = Habit.objects.get(id=habit_id)
        completed_habit = CompletedHabit.objects.filter(
            habit=habit,
            completed_date=date,
        ).first()

        # if it's not in the db, put it in there
        if completed_habit is None:
            CompletedHabit.objects.create(
                habit=habit,
                completed_date=date,
            ) 
        else:
            # if it is in db, delete it
            completed_habit.delete()

        return redirect('habits')

    return render(request, 'habits/completed.html')
