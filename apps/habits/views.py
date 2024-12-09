from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, HabitForm, CompletedForm
from .models import Habit, User, CompletedHabit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse

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
        date_strs = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            date_str = f"{date.strftime('%a').upper()} {date.strftime('%d')}"
            dates.append(date)
            date_strs.append(date_str)
        dates.reverse()
        date_strs.reverse()

        # For Displaying already completed habits
        completed_habits = CompletedHabit.objects.filter(habit__in=habits, completed_date__in=dates)  # only get the completed habits that match our habits/dates we are displaying
        
        # Store completion status for each habit 
        completion_status = {}
        
        for habit in habits :
            habit_key = f"{habit.id}"
            # Nested dict for each habit 
            completion_status[habit.id] = {}

            # Get completion records for current habit 
            completion_records = CompletedHabit.objects.filter(
                habit=habit,
                completed_date__in=dates
            )

            # Get dates habit was completed
            completion_dates = {
                record.completed_date.strftime('%Y-%m-%d')
                for record in completion_records 
            }

            # For dashboard dates, store whether or not they were completed
            for date in dates:
                date_str = date.strftime('%Y-%m-%d')
                # if date_str in completion_dates, create nested dict entry for habit
                # stores bool
                completion_status[habit.id][date_str] = date_str in completion_dates
        
        habit_form = HabitForm()
# 
        # Context passed into template
        context = {
            'habits': habits,
            'dates': dates,
            'habit_form': habit_form,
            'date_strings': date_strs,
            'completed_habits': completed_habits,
            'completion_status': completion_status
        }


    return render(request, 'habits/habits.html', context)
    

# COMPLETED HABITS ---------------------------------

def completed(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        date = request.POST.get('date')
        print("Received POST with habit_id:", habit_id, "and date:", date)

        cleaned_date = date.replace('a.m', 'AM').replace('p.m', 'PM')
        date_obj = datetime.strptime(cleaned_date, '%b. %d, %Y, %I:%M %p.').date()
        print("Converted to date_obj:", date_obj)

        # Search through instances of Habit to find the one with matching id
        habit = Habit.objects.get(id=habit_id)
        print('Habit:', habit.name, habit.date_created)
        completed_habit = CompletedHabit.objects.filter(
            habit=habit,
            completed_date=date_obj,
        ).first() 

        # For JSON res
        status = False
        
        # if it's in the db, remove it
        if completed_habit is not None:
            print("Deleting completed habit")
            completed_habit.delete() 
            status = False

        # if it's not in the db, create a record
        else:
            print(f"Creating new completed habit with date completed date = {date_obj}")
            CompletedHabit.objects.create(
                habit=habit,
                completed_date=date_obj,
            ) 
            status = True

        return JsonResponse({'status': status}) 

    return JsonResponse({'error': 'Invalid request'}, status=400)
