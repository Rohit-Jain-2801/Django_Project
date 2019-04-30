from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo,GWL_inputs,Site_Name,FYear,City

# from django.contrib.auth.forms import UserCreationForm
# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     class Meta():
#         model = User
#         fields = ['username','email','password1','password2']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class UserUpdateForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class GWL(forms.ModelForm):
    class Meta():
        model = GWL_inputs
        fields = ('state','district','block',)

class Site(forms.ModelForm):
    class Meta():
        model = Site_Name
        fields = ('site',)

class Year(forms.ModelForm):
    class Meta():
        model = FYear
        fields = ('year',)

class CityForm(forms.ModelForm):
    class Meta:
        model = City 
        fields = ['name',]
        widgets = {'name' : forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}