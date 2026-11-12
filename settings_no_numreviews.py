from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)

SESSION_CONFIGS = [
    # PILOT: 20 shoes per gender, fake (deterministic) star reviews, response-curve page shown
    dict(
        name='multiattr_pilot',
        display_name='Multi-attribute PILOT (placeholder reviews)',
        num_demo_participants=1,
        app_sequence=['binarychoice'],
        prolificurl='',
        pilot=1,
        use_placeholder_reviews=1,
    ),
    # REAL STUDY: all shoes, real reviews from binarychoice/shoe_reviews.csv (must be fully filled in)
    dict(
        name='multiattr_study',
        display_name='Multi-attribute STUDY',
        num_demo_participants=None,
        app_sequence=['binarychoice'],
        prolificurl='',  # fill in the Prolific completion URL before collecting data
        pilot=0,
        use_placeholder_reviews=0,
    ),
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
