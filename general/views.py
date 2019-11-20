from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import *
from .models import *


class PicsList(View):
	def get(self, request):
		photos = Photo.objects.all()
		form = PicsListForm
		return render(request, 'general/pics_list.html', context={'photos': photos, 'form': form, 'post': False})

	def post(self, request):
		form = PicsListForm
		title = request.POST['title']
		photos = Photo.objects.filter(title__icontains=title)
		return render(request, 'general/pics_list.html', context={'photos': photos, 'form': form, 'post': True})

class UserList(View):
	def get(self, request):
		form = UserListForm
		users = User.objects.all()
		return render(request, 'general/users_list.html', context={'users': users, 'form': form, 'post': False})

	def post(self, request):
		form = UserListForm
		name = request.POST['username']
		users = User.objects.filter(title__icontains=name)
		return render(request, 'general/users_list.html', context={'users': users, 'form': form, 'post': True})

def users_list(request):
	users = User.objects.all()
	return render(request, 'general/users_list.html', context={'users': users})


class NewUser(View):
	 def get(self, request):
	 	form = CustomUserForm
	 	return render(request, 'general/new_user.html', context={'form': form})

	 def post(self, request):
	 	form = CustomUserForm(request.POST)
	 	if form.is_valid():
	 		form.save()
	 		username = request.POST.get('username')
	 		password = request.POST.get('password1')	 		
	 		user = authenticate(request, username=username, password=password)
	 		login(request, user)
	 		return redirect('pics_list_url')
	 	else:
	 		return render(request, 'general/new_user.html', context={'form': form})

class LoginUser(View):
	def get(self, request):
		form = LoginForm
		return render(request, 'general/user_login.html', context={'form': form})

	def post(self, request):	 	
	 	username = request.POST['username']
	 	password = request.POST['password']
	 	user = authenticate(request, username=username, password=password)
	 	if user is not None:
	 		login(request, user)
	 		return redirect('pics_list_url')
	 	else:
	 		form = LoginForm
	 		return render(request, 'general/user_login.html', context={'form': form})

def user_logout(request):
	logout(request)
	return redirect('pics_list_url')

class UserDetail(View):
	def get(self, request, username):
		user = get_object_or_404(User, username__iexact = username)
		return render(request, 'general/user_detail.html', context={'user': user})

class PhotoUpload(View):
	def get(self, request):
		if request.user.username:
			form = PhotoForm
			return render(request, 'general/photo_upload.html', context={'form': form})
		else:
			return redirect('pics_list_url')

	def post(self, request):
		form = PhotoForm(request.POST, request.FILES)

		if form.is_valid():
			if Photo.objects.filter(user = request.user).count() > 0:
				request.user.photo.delete()
			photo = Photo.objects.create(user = request.user)
			photo.title = request.POST['title']
			photo.description = request.POST['description']
			photo.file = request.FILES['file']
			photo.save()
			request.user.user_add.counter += 1
			request.user.user_add.save()			
			return redirect('pics_list_url')

		else:
			return render(request, 'general/photo_upload.html', context={'form': form})

class UserDelete(View):
	def get(self, request, username):
		user = get_object_or_404(User, username__iexact=username)
		if user == request.user:
			form = UserDeleteForm()
			return render(request, 'general/user_delete_form.html', context={'form': form, 'user': user})
		else:
			return redirect('pics_list_url')

	def post(self, request, username):
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			user.delete()
			return redirect('pics_list_url')		
		else:
			form = UserDeleteForm()
			return render(request, 'general/user_delete_form.html', context={'form': form, 'user': user})

class PicDetail(View):
	def get(self, request, id):
		photo = get_object_or_404(Photo, id = id)
		return render(request, 'general/pic_detail.html', context={'photo':photo})

class PicDelete(View):
	def get(self, request, id):
		photo = get_object_or_404(Photo, id=id)
		form = PicDeleteForm()
		if photo.user == request.user:
			return render(request, 'general/pic_delete.html', context = {'form':form, 'photo':photo})
		else:
			return redirect('pic_detail_url', id=photo.id)

	def post(self, request, id):
		photo = get_object_or_404(Photo, id=id)
		photo.delete()
		return redirect('pics_list_url')

class UserEdit(View):
	def get(self, request, username):
		user = get_object_or_404(User, username=username)
		if request.user == user:
			form = UserEditForm
			return render(request, 'general/user_edit.html', context={'form': form, 'user': user})
		else:
			return redirect('user_detail_url', username= user.username)

	def post(self,request, username):
		user = get_object_or_404(User, username=username)		
		user.user_add.description = request.POST['description']
		user.user_add.save()
		return redirect('user_detail_url', username= user.username)

def about(request):
	return render(request, 'general/about.html')

def admin_delete_pic(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		photo = get_object_or_404(Photo, id=id)
		photo.delete()
		return redirect('pics_list_url')
	else:
		return redirect('pics_list_url')

def admin_delete_user(request, username):
	if request.user.is_authenticated and request.user.is_staff:
		user = get_object_or_404(User, username=username)
		user.delete()
		return redirect('pics_list_url')
	else:
		return redirect('pics_list_url')

class AdminUsersList(View):
	def get(self, request):
		form = UserListForm
		users = User.objects.all()
		return render(request, 'general/admin_users_list.html', 
						context={'form': form, 'users': users, 'post': False})

	def post(self, request):
		form = UserListForm
		name = request.POST['username']
		users = User.objects.filter(username__icontains=name)
		return render(request, 'general/admin_users_list.html', 
						context={'form': form, 'users': users, 'post': True})

class AdminPicsList(View):
	def get(self, request):
		form = PicsListForm
		photos = Photo.objects.all
		return render(request, 'general/admin_pics_list.html', 
						context={'form': form, 'photos': photos, 'post': False})

	def post(self, request):
		form = PicsListForm
		title = request.POST['title']
		photos = Photo.objects.filter(title__icontains=title)
		return render(request, 'general/admin_pics_list.html', 
						context={'form': form, 'photos': photos, 'post': True})