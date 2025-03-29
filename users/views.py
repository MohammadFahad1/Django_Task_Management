from ast import Assign
from email import message
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import CustomRegistrationForm, LoginForm, RegisterForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test

# Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

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
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'registration/login.html', {"form": form})
        # username = request.POST.get('username')
        # password = request.POST.get('password')

        # user = authenticate(request, username=username, password=password)

        # if user is not None:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     messages.error(request, "Invalid username or password")
        
    # return render(request, 'registration/login.html')

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
    
def activate_user(request, user_id, token):
    user = User.objects.get(id=user_id)
    try:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully.")
            return redirect('sign-in')
        else:
            messages.error(request, "Invalid activation link")
            return redirect('sign-in')
    except User.DoesNotExist:
        messages.error(request, "Invalid activation link")
        return redirect('sign-in')


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {"users": users})

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Clear existing roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} role has been changed to {role.name} role.")
            return redirect('admin-dashboard')
        
    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()

    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully.")
            return redirect('create-group')
    
    return render(request, 'admin/create_group.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {"groups": groups})

""" 
    Admin
        - Sobkisui
    Manager
        - Project
        - Task Create
    Employee
        - Task read
        - Task update
    
        Role Based Access Control (RBAC)

        https://medium.com/@fahimad/role-based-access-control-rbac-in-django-1955b31d93a5
        https://docs.djangoproject.com/en/5.1/topics/auth/
"""