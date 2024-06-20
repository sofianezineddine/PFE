from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import  User,Profile





class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username","class":"input_field","id":"input_field","required":""}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"name@mail.com","class":"input_field","id":"input_field"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"input_field","id":"input_field"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password","class":"input_field","id":"input_field"}))
    
    class Meta:
        model = User
        fields = ['username','email']





class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']