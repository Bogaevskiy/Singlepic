import random, string

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
