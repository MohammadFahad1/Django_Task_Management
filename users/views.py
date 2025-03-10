from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.forms import CustomRegistrationForm, RegisterForm

# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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