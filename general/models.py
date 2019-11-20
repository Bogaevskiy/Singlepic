from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.contrib.auth.models import User

class User_add(models.Model):
	description = models.TextField(blank=True, default = "")
	counter = models.IntegerField(default=0)
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)


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

	def __str__(self):
		return self.title