from django.shortcuts import render

# simple view that renders a template
def home(request):
    return render(request, 'habits/home.html')
    
