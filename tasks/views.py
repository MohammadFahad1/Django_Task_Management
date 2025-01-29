from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hello, world. You're at the home page now.")

def contact(request):
    return HttpResponse("<h1 style='color:red; font-family:calibri'>Welcome to the contact page</h1>")

def show_task(request):
    return HttpResponse("<h1>Welcome to the <span style='color:red; font-family:calibri'>show task</span> page</h1>")