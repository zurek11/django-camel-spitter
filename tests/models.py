from django.db import models
from camel_spitter.models import BaseLogModel


class BasicLogEntry(BaseLogModel):
    class Meta:
        app_label = 'tests'
        db_table = 'log_entries'
        default_permissions = ()


class ExtendedLogEntry(BaseLogModel):
    class Meta:
        app_label = 'tests'
        db_table = 'extended_log_entries'
        default_permissions = ()

    special = models.CharField(max_length=50, null=False, default='')
    user = models.CharField(max_length=50, null=False, default='')
    amount = models.IntegerField(null=False, default=1)
