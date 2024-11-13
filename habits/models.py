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
