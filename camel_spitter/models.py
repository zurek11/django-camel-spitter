from django.db import models


class BaseLogModel(models.Model):
    class Meta:
        abstract = True

    level = models.CharField(max_length=50, null=False, default='')
    module = models.CharField(max_length=50, null=False, default='')
    function = models.CharField(max_length=50, null=False, default='')
    filename = models.CharField(max_length=50, null=False, default='')
    message = models.TextField(null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
