import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.fields import RegisterEmailField, ConfirmationCodeField
from groupapp.croppable.forms import CroppableImageField
from groupapp.models import UserProfile
            
class EmailForm(forms.Form):
    email = RegisterEmailField(label="Company Email")
    
class ConfirmationCodeForm(forms.Form):
    confirmation_code = ConfirmationCodeField(label="Confirmation Code")

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=200, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=200, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    cpassword = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    picture = CroppableImageField(required=False, label="Picture")
    
    def clean_cpassword(self):
        if not 'password' in self.cleaned_data or self.cleaned_data['cpassword'] != self.cleaned_data['password']:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
        
class UserEditForm(forms.Form):
    first_name = forms.CharField(max_length=200, label="First Name")
    last_name = forms.CharField(max_length=200, label="Last Name")
    picture = CroppableImageField(required=False, label="Picture")

class UserEditModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200, label="First Name")
    last_name = forms.CharField(max_length=200, label="Last Name")
    picture = CroppableImageField(required=False, label="Picture")

    class Meta:
        model = UserProfile
        fields = ('picture',)
        #exclude = ('organization', 'is_administrator', 'latest_status', 'user')

    #first_name = forms.CharField(max_length=200, label="First Name")
    #last_name = forms.CharField(max_length=200, label="Last Name")
    #picture = CroppableImageField(required=False, label="Picture")
    
class OrganizationForm(forms.Form):
    name = forms.CharField(max_length=100)
    #domain = DomainField(max_length=100, required=False)
    
class LoginForm(AuthenticationForm):
    '''
        Extended so it automatically places placeholders
    '''
    username = forms.EmailField(label="Company Email", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))