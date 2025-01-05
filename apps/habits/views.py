from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, HabitForm, CompletedForm
from .models import Habit, User, CompletedHabit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import calendar
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.http import JsonResponse, Http404
from html.parser import HTMLParser
from bs4 import BeautifulSoup

User = get_user_model()

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

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
# Handles habit creation/listing
@login_required
def habits(request):
    User = get_user_model()
    
    # POST
    if request.method == 'POST':
        habit_form = HabitForm(request.POST)
        if habit_form.is_valid():
            # Create new habit
            habit = habit_form.save(commit=False) # "pause" save 
            habit.user = request.user # associate user with habit
            habit.save() # complete save to db
            return redirect('habits')

    # GET
    else:
        # Habits for dashboard table:
        habits = Habit.objects.filter(user=request.user) # find user's habits
        
        # Dates for dashboard table:
        today = datetime.today()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)] # The most recent 7 days
        dates.reverse()
        date_strs = [d.strftime('%a %d').upper() for d in dates]
        
        # For Displaying already completed habits
        completed_habits = CompletedHabit.objects.filter(habit__in=habits, completed_date__in=dates)  # only get the completed habits that match our habits/dates we are displaying
        
        # Store completion status for each habit 
        completion_status = {}
        
        for habit in habits :
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
                completion_status[habit.id][date_str] = date_str in completion_dates # stores bool
        
        habit_form = HabitForm()

        # Context passed into template
        context = {
            'habits': habits,
            'dates': dates,
            'habit_form': habit_form,
            'date_strings': date_strs,
            'completed_habits': completed_habits,
            'completion_status': completion_status,
        }

    return render(request, 'habits/habits.html', context)

    
# HABIT DELETION -----------------------------------
def delete_habit(request, habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        habit.delete()
    except Habit.DoesNotExist:
        raise Http404("Non existant habit.")

    return redirect('habits')


# INDIVIDUAL HABITS --------------------------------
    # Simple analytics for each of the user's habits

def details(request, habit_id):
    # Find habit associated with current id
    habit = Habit.objects.get(id=habit_id)

    print(habit.name)

    completed_habits = CompletedHabit.objects.filter(
        habit=habit
    ).order_by('-completed_date')

    print(completed_habits[0].completed_date)

    # Completion Rate
    days = (timezone.now().date() - habit.date_created.date()).days + 1 # Days since habit was created
    total_complete = completed_habits.count()
    rate = round(((total_complete / days) * 100 if days > 0 else 0), 0) 

    print(f"Rate: {rate}")

    # Streak
    current_streak = 0
    if completed_habits.exists():
        current_date = completed_habits.first().completed_date # most recent

        for c in completed_habits:
            if c.completed_date == current_date:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break

    print(f"Streak: {current_streak}")

    # Weekly counts bar graph
    # TODO: get completed habit count for each week since creation
    # TODO: create bar graph - library?
    
    # Calendar - shows completion for each day of the month
    # TODO: MAKE BETTER - validation, testing, multiple months, etc
    html_cal = calendar.HTMLCalendar().formatmonth(datetime.now().year, datetime.now().month)
    
    soup = BeautifulSoup(html_cal, 'lxml')

    # parse day cells
    tds = soup.find_all('td')

    completed_dates = [] 
    for ch in completed_habits:
        completed_dates.append(str(ch.completed_date.day))

    completed_dates.reverse()

    # Check if day has been completed
    for td in tds:
        if str(td.string) in completed_dates:
           td['class'] = 'cal-completed'
    
    context = {
        'habit_id': habit_id,
        'habit': habit,
        'rate': rate,
        'streak': current_streak,
        'cal': mark_safe(soup.prettify), # mark_safe - allows HTML to render in template
    }

    return render(request, 'habits/details.html', context) 

# COMPLETED HABITS ---------------------------------

def completed(request):
    if request.method == 'POST':
        status = False # For JSON response
        habit_id = request.POST.get('habit_id')

        date = request.POST.get('date')
        cleaned_date = date.replace('a.m', 'AM').replace('p.m', 'PM')
        date_obj = datetime.strptime(cleaned_date, '%b. %d, %Y, %I:%M %p.').date()
        print("Date Object: ", date_obj)

        # Search through instances of Habit to find the one with matching id
        habit = Habit.objects.get(id=habit_id)
        completed_habit = CompletedHabit.objects.filter(
            habit=habit,
            completed_date=date_obj,
        ).first() 

        # if it's in the db, remove it
        if completed_habit is not None:
            completed_habit.delete() 
            status = False
            print("habit deleted")

        # if it's not in the db, create a record
        else:
            CompletedHabit.objects.create(
                habit=habit,
                completed_date=date_obj,
            ) 
            status = True
            print('habit created')

        return JsonResponse({'status': status}) 

    return JsonResponse({'error': 'Invalid request'}, status=400)


# TODO: Add try/excepts for practice error checking
# TODO: Refactor views to use Classes