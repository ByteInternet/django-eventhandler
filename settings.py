INSTALLED_APPS = (
    'eventhandler',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = 'my_secret_key'

LISTENER_URL = None
LISTENER_QUEUE = None
LISTENER_EXCHANGE = None
LISTENER_TOPIC = 'topic'
LISTENER_ROUTING_KEY = '#'
