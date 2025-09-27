from operator import ge
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Permission, Group
from django import forms
import re
from tasks.forms import StyledFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'confirm_password']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists.")
        
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append("Password must be at least 8 character long.")
        # elif re.fullmatch(r'[A-Za-z0-9@#%^&+=]', password1):
        #     errors.append("Password must include uppercase, lowercase, numeric and special characters.")
        if not re.search(r'[A-Z]', password1):
            errors.append("Password must include at least one uppercase letter.")
        
        if not re.search(r'[a-z]', password1):
            errors.append("Password must include at least one lowercase letter.")

        if not re.search(r'[0-9]', password1):
            errors.append("Password must include at least one number.")

        if not re.search(r'[@#$%^&*+=]', password1):
            errors.append("Password must include at least one special character.")
        
        if errors:
            raise forms.ValidationError(errors)

        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match.")

class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass


class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image', 'location', 'birth_date'] 

"""
class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
    
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    location = forms.CharField(max_length=100, required=False, label="Location")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Birth Date")

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_images
            self.fields['location'].initial = self.userprofile.location
            self.fields['birth_date'].initial = self.userprofile.birth_date
    
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_images = self.cleaned_data.get('profile_image')
            self.userprofile.location = self.cleaned_data.get('location')
            self.userprofile.birth_date = self.cleaned_data.get('birth_date')
            
            if commit:
                self.userprofile.save()

        if commit:
            user.save()

        return user
"""