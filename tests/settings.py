import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'camel_spitter',
    'tests',
)

DATABASE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    },
    'logging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
        'TEST': {
            'MIRROR': 'default',
        }
    },
}

MIDDLEWARE = []

USE_TZ = True
TIME_ZONE = 'UTC'
SECRET_KEY = 'g>Q3Y>VDJ7s};)-g>2Csjz&7FYRm"F?A@QX#"<AXlJfC>a!v&GTL[ey]nE`?cJL'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'db_filter': {
            '()': 'camel_spitter.db_filter.DBFilter',
        },
    },
    'handlers': {
        'db': {
            'level': 'INFO',
            'class': 'camel_spitter.db_handler.DBHandler',
            'model': 'tests.models.BasicLogEntry',
            'filters': ['db_filter']
        }
    },
    'loggers': {
        'logger': {
            'handlers': ['db'],
            'level': 'INFO'
        }
    }
}
