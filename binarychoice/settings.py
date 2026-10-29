from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [
		dict(name='study1_shoes', 
			num_demo_participants=None, 
			app_sequence=['binarychoice_twobuttons'], 
			prolificurl='', 
			pilot=0), 
		dict(name='study2', 
			num_demo_participants=None, 
			app_sequence=['moneyrisk'], 
			pilot=0, 
			prolificurl='')
]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
THOUSAND_SEPARATOR = ''
AUTO_TABULATE_PAYOFFS = True
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


