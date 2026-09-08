from os import environ


SESSION_CONFIGS = [
    dict(
        name='finland_appearance_poc',
        display_name='Political appearance in Finland — proof of concept',
        app_sequence=['appearance_experiment'],
        num_demo_participants=1,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc='',
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
DEMO_PAGE_INTRO_HTML = ''
SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'appearance-poc-local-development')
