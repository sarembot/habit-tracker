from django.urls import path, include
from habits import views

urlpatterns = [
    path('', views.home, name="home"),

    # Habits
    path('habits', views.habits, name="habits"),

    # Registration
    path('registration/login', views.login, name="login"),
    path('registration/signup', views.signup, name="signup"),
    path('registration/success', views.success, name="success")
]
