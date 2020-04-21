from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.paginator import Paginator

from django.core.mail import send_mail #to delete later

from django.conf import settings


from .utils import *
from .forms import *
from .models import *


def landing(request):
	if request.user.is_authenticated:
		return redirect("pics_list_url")
	else:
		return render(request, 'general/landing.html')

class PicsList(View):
	def get(self, request):
		photos = Photo.objects.all().order_by('-id')
		form = PicsListForm

		paginator = Paginator(photos, 4)
		page_number = request.GET.get('page', 1)
		page = paginator.get_page(page_number)
		is_paginated = page.has_other_pages()

		if page.has_previous():
			prev_url = '?page={}'.format(page.previous_page_number())
		else:
			prev_url = ''

		if page.has_next():
			next_url = '?page={}'.format(page.next_page_number())
		else:
			next_url = ''

		context = {
			'photos': photos,
			'form': form,
			'post': False,
			"page_object": page,
			"is_paginated": is_paginated,
			"prev_url": prev_url,
			"next_url": next_url
			}
		return render(request, 'general/pics_list.html', context=context)

	def post(self, request):
		form = PicsListForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			photos = Photo.objects.filter(title__icontains=title).order_by('id')
		else:
			photos = Photo.objects.all().order_by('id')		

		paginator = Paginator(photos, 4)
		page_number = request.GET.get('page', 1)
		page = paginator.get_page(page_number)
		is_paginated = page.has_other_pages()

		if page.has_previous():
			prev_url = '?page={}'.format(page.previous_page_number())
		else:
			prev_url = ''

		if page.has_next():
			next_url = '?page={}'.format(page.next_page_number())
		else:
			next_url = ''

		context={
			'photos': photos,
			'form': form,
			'post': True,
			"page_object": page,
			"is_paginated": is_paginated,
			"prev_url": prev_url,
			"next_url": next_url
		}

		return render(request, 'general/pics_list.html', context=context)

class UserList(View):
	def get(self, request):
		form = UserListForm
		users = User.objects.all()
		return render(request, 'general/users_list.html', context={'users': users, 'form': form, 'post': False})

	def post(self, request):
		form = UserListForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['username']
			users = User.objects.filter(username__icontains=name)
		else:
			users = User.objects.all()		
		return render(request, 'general/users_list.html', context={'users': users, 'form': form, 'post': True})

class NewUser(View):
	 def get(self, request):
	 	form = CustomUserForm
	 	return render(request, 'general/new_user.html', context={'form': form})

	 def post(self, request):
	 	form = CustomUserForm(request.POST)
	 	if form.is_valid():
	 		form.save()
	 		username = form.cleaned_data['username']
	 		password = form.cleaned_data['password1']	 			 		
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
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
		else:
			return render(request, 'general/user_login.html', context={'form': form})
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('pics_list_url')
		else:
			form = LoginForm
			return render(request, 'general/user_login.html', context={'form': form})	 	

def user_logout(request):
	logout(request)
	return redirect('landing_url')

class UserDetail(View):
	def get(self, request, username):
		user = get_object_or_404(User, username__iexact = username)
		if request.user.is_authenticated:
			sub_exist = Subscription.objects.filter(user = request.user, friend = user)
		else:
			sub_exist = False
		return render(request, 'general/user_detail.html', context={'user': user, 'sub_exist': sub_exist})

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
			photo.title = form.cleaned_data['title']			
			photo.description = form.cleaned_data['description']
			photo.file = request.FILES['file']
			photo.save()

			notification = Notification.objects.create()
			notification.body = '{0} has uploaded new pic - {1}'.format(request.user.username, photo.title)
			notification.save()
			subs = Subscription.objects.filter(friend = request.user)
			for sub in subs:
				notification.user.add(sub.user)

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
		form = UserDeleteForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			user = authenticate(request, username = username, password = password)
			if user is not None:
				user.delete()
				return redirect('pics_list_url')		
			else:
				form = UserDeleteForm()
				return render(request, 'general/user_delete_form.html', context={'form': form, 'user': user})
		else:
			return redirect('user_delete_url')

class PicDetail(View):
	def get(self, request, id):
		form = CommentForm()
		photo = get_object_or_404(Photo, id = id)
		counter = Like.objects.filter(photo = photo).count()
		comments = Comment.objects.filter(photo = photo)
		if request.user.is_authenticated:
			like_exist = Like.objects.filter(photo = photo, user = request.user)
		else:
			like_exist = False
		block_message = blockedcommentmessage()
		return render(request, 'general/pic_detail.html', 
						context={'photo':photo, 
						'counter': counter, 
						'like_exist': like_exist, 
						'form': form, 
						'comments': comments,
						'block_message': block_message})

	def post(self, request, id):		
		photo = get_object_or_404(Photo, id = id)	
		form = CommentForm(request.POST)
		if form.is_valid():	
			comment = Comment.objects.create(photo = photo, user = request.user)
			comment.author = request.user.username
			comment.body = form.cleaned_data['body']		
			comment.save()
			
			notification = Notification.objects.create()
			notification.user.add(photo.user)
			notification.body = '{0} has commented your pic'.format(request.user.username)
			notification.save()

			photo.comments_counter = Comment.objects.filter(photo = photo).count()
			photo.save()	
		if request.user.is_authenticated:
			like_exist = Like.objects.filter(photo = photo, user = request.user)
		else:
			like_exist = False
		return redirect('pic_detail_url', id=id)
		

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
			form = UserEditForm(description = user.user_add.description)
			return render(request, 'general/user_edit.html', context={'form': form, 'user': user})
		else:
			return redirect('user_detail_url', username= user.username)

	def post(self,request, username):		
		user = get_object_or_404(User, username=username)	
		form = UserEditForm(request.POST, description = user.user_add.description)
		if form.is_valid():			
			user.user_add.description = form.cleaned_data['description']			
			user.user_add.save()
		return redirect('user_detail_url', username= user.username)

class UserBaseEdit(View):
	def get(self, request, username):
		user = get_object_or_404(User, username=username)		
		if request.user == user:
			form = UserBaseEditForm(mail = user.email)
			return render(request, 'general/user_base_edit.html', context={'form': form, 'user': user})
		else:
			return redirect('user_detail_url', username=user.username)			

	def post(self, request, username):
		user = get_object_or_404(User, username=username)
		form = UserBaseEditForm(request.POST, mail = user.email)
		if form.is_valid():
			user = get_object_or_404(User, username=username)
			password = form.cleaned_data['password']
			user = authenticate(request, username = username, password = password)		
			if user is not None and request.user == user:
				email = form.cleaned_data['email']
				r = User.objects.filter(email = email)
				if r.count() and user.email != email:
					raise ValidationError("This E-mail is already in use")
				else:
					user.email = email
				newpassword1 = form.cleaned_data['newpassword1']
				newpassword2 = form.cleaned_data['newpassword2']
				if newpassword1 != newpassword2:
					raise ValidationError("Something wrong with new password")
				else:
					user.set_password(newpassword1)
				user.save()
				login(request, user)
		return redirect('user_detail_url', username= user.username)

def about(request):	
	return render(request, 'general/about.html')

def admin_delete_pic(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		photo = get_object_or_404(Photo, id=id)
		photo.delete()

		notification = Notification.objects.create()
		notification.user.add(photo.user)
		notification.body = 'Admin has deleted your pic'
		notification.save()

		return redirect('pics_list_url')
	else:
		return redirect('pics_list_url')

def admin_block_pic(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		photo = get_object_or_404(Photo, id=id)
		photo.blocked = not photo.blocked
		photo.save()

		notification = Notification.objects.create()
		notification.user.add(photo.user)
		notification.body = 'Admin has blocked your pic'
		notification.save()
	return redirect("pic_detail_url", id=id)

def admin_delete_user(request, username):
	if request.user.is_authenticated and request.user.is_staff:
		user = get_object_or_404(User, username=username)
		user.delete()
	return redirect('pics_list_url')	

def admin_block_comment(request, comm_id, pic_id):
	if request.user.is_authenticated and request.user.is_staff:
		comment = get_object_or_404(Comment, id=comm_id)
		comment.blocked = not comment.blocked
		comment.save()
	return redirect("pic_detail_url", id=pic_id)

def admin_delete_comment(request, comm_id, pic_id):
	if request.user.is_authenticated and request.user.is_staff:
		comment = get_object_or_404(Comment, id=comm_id)
		comment.delete()
	return redirect("pic_detail_url", id=pic_id)	

class AdminUsersList(View):
	def get(self, request):
		if request.user.is_authenticated and request.user.is_staff:
			form = UserListForm
			users = User.objects.all()
			return render(request, 'general/admin_users_list.html', 
							context={'form': form, 'users': users, 'post': False})
		else:
			return redirect('pics_list_url')

	def post(self, request):
		if request.user.is_authenticated and request.user.is_staff:
			form = UserListForm(request.POST)
			if form.is_valid():
				name = form.cleaned_data['username']
				users = User.objects.filter(username__icontains=name)
			else:
				users = User.objects.all()
			return render(request, 'general/admin_users_list.html', 
							context={'form': form, 'users': users, 'post': True})
		else:
			return redirect('pics_list_url')

class AdminPicsList(View):
	def get(self, request):
		if request.user.is_authenticated and request.user.is_staff:
			form = PicsListForm
			photos = Photo.objects.all()
			return render(request, 'general/admin_pics_list.html', 
							context={'form': form, 'photos': photos, 'post': False})
		else:
			return redirect('pics_list_url')

	def post(self, request):
		if request.user.is_authenticated and request.user.is_staff:
			form = PicsListForm(request.POST)
			if form.is_valid():
				title = form.cleaned_data['title']
				photos = Photo.objects.filter(title__icontains=title)
			else:
				photos = Photo.objects.all()
			return render(request, 'general/admin_pics_list.html', 
							context={'form': form, 'photos': photos, 'post': True})
		else:
			return redirect('pics_list_url')

class AdminCommentsList(View):
	def get(self, request):
		if request.user.is_authenticated and request.user.is_staff:
			form = CommentsListForm
			comments = Comment.objects.all()
			return render(request, 'general/admin_comments_list.html',
							context = {'form': form, 'comments': comments, 'post': False})

	def post(self, request):
		if request.user.is_authenticated and request.user.is_staff:
			form = CommentsListForm(request.POST)
			if form.is_valid():
				search = form.cleaned_data['search']
			author_comments = Comment.objects.filter(author__icontains = search)
			body_comments = Comment.objects.filter(body__icontains = search)
			return render(request, 'general/admin_comments_list.html',
							context = {
							'form': form,
							'author_comments': author_comments,
							'body_comments': body_comments,
							'post': True})


def user_subscribe(request, username):
	friend = User.objects.get(username=username)
	if request.user.is_authenticated and request.user != friend:
		subscription = Subscription.objects.create(user = request.user)
		subscription.friend = friend
		subscription.save()
	return redirect('user_detail_url', username=username)

def user_unsubscribe(request, username):
	friend = User.objects.get(username=username)
	if request.user.is_authenticated and request.user != friend:
		subscription = Subscription.objects.get(user = request.user, friend = friend)
		subscription.delete()
	return redirect('user_detail_url', username=username)

def subscriptions_list(request):
	if request.user.is_authenticated:
		subscriptions = Subscription.objects.filter(user = request.user)
		return render(request, 'general/subscriptions_list.html', context={'subscriptions': subscriptions})
	else:
		return redirect('pics_list_url')

def subs_pics_list(request):
	if request.user.is_authenticated:
		subscriptions = Subscription.objects.filter(user = request.user)
		return render(request, 'general/subs_pics_list.html', context={'subscriptions': subscriptions})
	else:
		return redirect('pics_list_url')

def photo_like(request, id):
	if request.user.is_authenticated and request.user != photo.user:
		photo = Photo.objects.get(id=id)
		like = Like.objects.create(photo = photo)
		like.user = request.user
		like.save()
	return redirect('pic_detail_url', id=id)

def photo_dislike(request, id):
	if request.user.is_authenticated and request.user != photo.user:
		photo = Photo.objects.get(id=id)
		like = Like.objects.get(photo = photo, user = request.user)
		like.delete()
	return redirect('pic_detail_url', id=id)

class RestoreAccess(View):
	def get(self, request):
		form = RestoreAccessForm
		return render (request, 'general/restore_access.html', context={'form': form})

	def post(self, request):
		form = RestoreAccessForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			mail = form.cleaned_data['mail']
			if User.objects.filter(username = username):
				user = User.objects.get(username = username)
				if user.email == mail:
					newpassword = passwordgenerator()
					send_password_mail(newpassword, user.email, user.username)
					user.set_password(newpassword)
					user.save()
					return render(request, 'general/restore_access_info.html')
				else:
					return render(request, 'general/wrong.html')
			else:
				return render(request, 'general/wrong.html')
		else:
			return redirect('restore_access_url')

def verify_user(request, username):
	user = get_object_or_404(User, username=username)
	send_verification_mail(user.user_add.token, user.email, user.username)
	return render(request, 'general/verified1.html', context={'user': user})

def verified_user(request, username, token):
	user = get_object_or_404(User, username=username)
	if user.user_add.token == token and user == request.user:
		user.user_add.verified = True
		user.user_add.save()
		return render(request, 'general/verified2.html', context = {'user': user})
	else:
		return render(request, 'general/wrong.html')

def notifications(request):
	if request.user.is_authenticated:
		notifications = Notification.objects.filter(user = request.user)
		return render(request, 'general/notifications.html', context={'notifications': notifications})
	else:
		return redirect('pics_list_url')