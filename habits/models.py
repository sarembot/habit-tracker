from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # BASICS - fname, lname, email
    email = models.EmailField(unique=True)

    # fix naming issue
    groups = models.ManyToManyField(
        'auth.Group',
        related_name = 'habit_users'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name = 'habit_users'
    )
    # TODO: ADVANCED FEATURES - habit history, analytics (streaks,etc)
    # TODO: METHODS - edit user info

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    # Attributes
    name = models.CharField(max_length=30) # habit name
    date_created = models.DateTimeField(auto_now_add=True)
    
    # use choices when you want the value to be limited to certain responses
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) #link habits to a user  
    
    # TODO: Methods - mark completed


# keep track of completed habits
class CompletedHabit(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)  
    completed_date = models.DateField(auto_now_add=True)

