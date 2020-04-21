import random, string

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings



def blockedcommentmessage():
	messages = [
		'Comment was blocked by admin',
		'Comment was eaten by Abyss',
		'Comment was sucked into the black hole',
		'Comment was dissolved in space',
		'Comment was stolen by evil spirits',
		"It was here, now it's not",
		'Comment has gone to see the Ancient One' ]
	return random.choice(messages)

def passwordgenerator():
	words_list = [
		'artificial', 'abstract',
		'brilliant', 'bohemian',
		'compulsive', 'chemical',
		'destructable', 'domestic',
		'efficient', 'estimated',
		'fortunate', 'friendly',
		'grateful', 'ghostly',
		'holographic', 'hopeful',
		'insecure', 'invisible',
		'jealous', 'jumping',
		'keyless', 'kindly',
		'limited', 'lurking',
		'mutual', 'mythical',
		'negative', 'narrative',
		'obedient', 'original',
		'primitive', 'protective',
		'questionable', 'qualified',
		'restrained', 'restricted',
		'sensitive', 'superior',
		'temporary', 'tempting',
		'unexpected', 'unbroken',
		'viscous', 'violent',
		'whitening', 'waiting',
		'xeroxed','yellow', 'zombified']
	number = random.randint(0, 9999)
	while len(str(number)) < 4:
		number = '0' + str(number)
	letters = ''
	for i in range(4):
		letters = letters + random.choice(string.ascii_letters)
	return random.choice(words_list).capitalize() + str(number) + letters

def send_password_mail(newpassword, email, username):		
	text = "Hello again. And thank you for using our restoring access system. Your new password is {}, hope to see you back soon".format(newpassword)
	msg = render_to_string('general/mail/restore_access.html', 
									context = {'newpassword': newpassword, 'username': username})
	send_mail(
		'Singlepic - restoring access',
		text,
		settings.EMAIL_HOST_USER,
		[email],
		html_message = msg
		)

def tokengenerator():
	token = ''
	for i in range(20):
		token += random.choice(string.ascii_letters + string.digits)
	return token

def send_verification_mail(token, email, username):
	text = "Hello again. To verify your account, use the included link. If you don't see it, then, something went wrong."
	msg = render_to_string('general/mail/verification.html', 
							context = {'username': username, 'token': token})
	send_mail(
		'Singlepic - verification',
		text,
		settings.EMAIL_HOST_USER,
		[email],
		html_message = msg
		)