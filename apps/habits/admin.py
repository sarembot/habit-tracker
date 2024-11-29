from django.contrib import admin
from .models import User, Habit, CompletedHabit

# Register your models here.

admin.site.register(Habit)
admin.site.register(User)
admin.site.register(CompletedHabit)
