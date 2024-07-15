from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_username', 'placeholder': 'Enter your username'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'id': 'id_password', 'placeholder': 'Enter your password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    
class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_first_name', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_last_name', 'placeholder': 'Enter your last name'}))
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput(attrs={'id': 'id_email', 'placeholder': 'Enter your email'}))
    username   = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'id_username', 'placeholder': 'Enter your username'}))
    password  = forms.CharField(max_length=200,
                                 label='Password', 
                                 widget=forms.PasswordInput(attrs={'id': 'id_password', 'placeholder': 'Enter your password'}))
    confirm  = forms.CharField(max_length=200,
                                 label='Confirm password',  
                                 widget=forms.PasswordInput(attrs={'id': 'id_confirm_password', 'placeholder': 'Confirm your password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username
    

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)
        widgets = {
            'picture': forms.FileInput(attrs={'id': 'id_profile_picture'})
        }
        labels = {
            'picture': ""
        }