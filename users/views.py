from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import CustomRegistrationForm, RegisterForm

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "A confirmation email has been sent to your email address. Please click on the link to activate your account.")
            return redirect('sign-in')
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password1')
        #     confirm_password = form.cleaned_data.get('password2')

        #     if password == confirm_password:
        #         User.objects.create(username=username, password=password)
        #     else:
        #         print("Password didn't matched.")
        else:
            print("form is not valid")
    
    return render(request, 'registration/register.html', {"form": form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
        
    return render(request, 'registration/login.html')

def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')