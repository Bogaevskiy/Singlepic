from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.contrib.auth.models import User

from django.utils import timezone

class User_add(models.Model):
	description = models.TextField(blank=True, default = "")
	counter = models.IntegerField(default=0)
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
	verified = models.BooleanField(default = False)
	token = models.CharField(max_length = 20, default = '')

	def __str__(self):
		return "Add to " + self.user.username


class Photo(models.Model):
	file = models.ImageField(upload_to = 'photos')
	thumbnail = ImageSpecField( source='file',
								processors=[ResizeToFill(300, 300)],
								format='JPEG', 
								options = {'quality': 90})	
	title = models.CharField(max_length = 50, db_index = True)
	description = models.TextField(max_length = 300)
	date_pub = models.DateTimeField(auto_now_add = True)
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	blocked = models.BooleanField(default = False)

	def __str__(self):
		return self.title

class Subscription(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	friend = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "friend", null = True)

	def __str__(self):
		return '{0} to {1}'.format(self.user.username, self.friend.username)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	photo = models.ForeignKey(Photo, on_delete = models.CASCADE, null = True)

	def __str__(self):
		return '{0} - {1}'.format(self.user.username, self.photo.title)

class Comment(models.Model):
	photo = models.ForeignKey(Photo, on_delete = models.CASCADE, null = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	author = models.CharField(max_length = 200, default = '')
	body = models.TextField(max_length = 200)
	created_at = models.DateTimeField(editable = False, default=timezone.now)
	blocked = models.BooleanField(default = False)

	def __str__(self):
		return '{0} com to {1}'.format(self.user.username, self.photo.title)