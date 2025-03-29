from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def no_permission(request):
    return render(request, 'no_permission.html')