from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile  


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='optional.')
	email = forms.EmailField(max_length=250, help_text='Required, please provide a valid email')


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
	profile_photo = forms.FileField(required=False, widget=forms.FileInput)
	class Meta:
		model = Profile
		fields = ('profile_photo','date_of_birth', 'id_number', 'location')


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


