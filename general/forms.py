from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


class CustomUserForm(forms.Form):
	username = forms.CharField(label='Your username', min_length = 3, max_length = 25)
	email = forms.EmailField(label='Your e-mail')
	password1 = forms.CharField(label='Enter your password', widget = forms.PasswordInput)
	password2 = forms.CharField(label='Confirm your password', widget = forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username']
		r = User.objects.filter(username = username.lower())
		if r.count():
			raise ValidationError("Same or similar username already exists")
		return username

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email = email)
		if r.count():
			raise ValidationError("This E-mail is already in use")
		return email

	def clean_password(self):
		password1 = self.cleaned_data.get(password1)
		password2 = self.cleaned_data.get(password2)
		if password1 and password2 and password1 != password2:
			raise ValidationError("Something wrong with password")
		return password1

	def save(self, commit = True):
		user = User.objects.create_user(
			self.cleaned_data['username'],
			self.cleaned_data['email'],
			self.cleaned_data['password1'])
		user_add = User_add.objects.create(user=user)
		user_add.save
		return user

class LoginForm(forms.Form):
	username = forms.CharField(label='Your username')
	password = forms.CharField(label='Password', widget = forms.PasswordInput)	

class PhotoForm(forms.Form):
	title = forms.CharField(label="Photo title")
	description = forms.CharField(label="Description", widget = forms.Textarea)
	file  = forms.ImageField(label="Your photo", widget = forms.FileInput)

class UserDeleteForm(forms.Form):
	password = forms.CharField(label='You need to enter your password')

class PicDeleteForm(forms.Form):
	pass

class UserEditForm(forms.Form):
	description = forms.CharField(label='Some words about yourself', widget = forms.Textarea)

class UserBaseEditForm(forms.Form):
	mail = "put something here"

	email = forms.EmailField(label="Your e-mail", initial = mail)
	newpassword1 = forms.CharField(label='Enter new password', widget = forms.PasswordInput)
	newpassword2 = forms.CharField(label='Confirm new password', widget = forms.PasswordInput)
	password = forms.CharField(label='Your current password', widget = forms.PasswordInput)





class UserListForm(forms.Form):
	username = forms.CharField(label='Search for users by name')

class PicsListForm(forms.Form):
	title = forms.CharField(label='Search pics by title')

class CommentForm(forms.Form):
	body = forms.CharField(label = "Your comment?")

class RestoreAccessForm(forms.Form):
	username = forms.CharField(label='Your username')
	mail = forms.EmailField(label='Your email')