from django.urls import path, include
from apps.habits import views

urlpatterns = [
    # Home
    path('', views.home, name="home"),

    # Registration
    path('registration/login', views.login, name="login"),
    path('registration/signup', views.signup, name="signup"),
    path('registration/success', views.success, name="success"),
    path('registration/logout', views.logout, name="logout"),

    # Habits
    path('habits', views.habits, name="habits"),
    path('habits/<int:habit_id>', views.details, name='details'),
    path('habits/delete/<int:habit_id>', views.delete_habit, name='delete_habit'),

    # Completed Habits
    path('completed', views.completed, name="completed")
]
