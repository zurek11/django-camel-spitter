# django-camel-spitter

[![codecov](https://codecov.io/gh/zurek11/django-camel-spitter/branch/master/graph/badge.svg)](https://codecov.io/gh/zurek11/django-camel-spitter)

<img src="media/logo.png" width="300">

Hi. I am a very rude camel 🐫 and I like to spit logs 💦 directly into your database 🗄️.

## Introduction

Project django-camel-spitter adds a new handler to standard django logging system.

Purpose of this handler is to store logs straight to the database, primary with simplicity and opportunity to easy extend this solution.

## Installation

```python
# pip
pip install django-camel-spitter

# pipenv
pipenv install django-camel-spitter

# poetry
poetry add django-camel-spitter
```

## Setup

#### 1. Adding `camel_spitter` to `settings.INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'camel_spitter'
)
```

#### 2. Adding additional `logging` db connection to `settings.DATABASES`:

> This additional connection is needed for handling DB transaction atomicity.
> Exception without own connection cannot create DB log, when rollback was made.
> Transactions in django are default handled on default DB connection.
> So rollback will stop default connection execution, but logging connection not.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', 5432),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', None)
    },
    'logging': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', 5432),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', None)
    }
}
```

#### 3. Adding `model`, `filter` and `handler` to `settings.LOGGING`:

```python
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
            'model': 'tests.models.BasicLogEntry',  # path to your custom model
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
```

#### 4. Creating a log model:

Only importance is inheritance from `camel_spitter.models.BaseLogModel`.

```python
from camel_spitter.models import BaseLogModel


class BasicLogEntry(BaseLogModel):
    class Meta:
        app_label = 'tests'
        db_table = 'log_entries'
        default_permissions = ()
```

## Example

#### 1. Quick use

If you did all setup steps, you are ready to log to the database.

```python
import logging
from app.models import BasicLogEntry

logging.getLogger('logger').error('Foo Bar Error')
logged_information = BasicLogEntry.objects.get(message='Foo Bar Error')

# logged_information = {BasicLogEntry}BasicLogEntry object (1)
```

---

#### 2. Example of extended model

If you like to log some additional data, for example: [request.body, user_name], you need to first add these fields to model:

```python
from camel_spitter.models import BaseLogModel
from django.db import models

class ExtendedLogEntry(BaseLogModel):
    class Meta:
        app_label = 'tests'
        db_table = 'extended_log_entries'
        default_permissions = ()

    request_body = models.JSONField(null=True)
    user_name = models.CharField(max_length=100, null=True)
```

As a second, you need to add these additional data to logging:

```python
import logging

logging.getLogger('logger').error('Foo Bar Error', extra={
    'request_body': json.loads(request.body), 'user_name': 'Foo Bar'
})
```

## Important notes

#### Testing with pytest and file DB

> When tests are made with pytest library and file DB like SQLite,
> tests will make two separate database files from specified connections even though path and engine are the same.
> So retrieving log is needed to be executed with using like `BasicLogEntry.objects.using('logging').get(message='Foo Bar')`.
> To avoid this issue you can specify mirror database in test settings.

```python
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
    },
    'logging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
        'TEST': {
            'MIRROR': 'default',
        }
    },
```

---
Made with ❤ by [Adam Žúrek](https://zurek11.github.io/) & [BACKBONE s.r.o.](https://www.backbone.sk/en/)
