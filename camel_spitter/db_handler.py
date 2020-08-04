from logging import Handler
from django.db import IntegrityError


class DBHandler(Handler):
    def __init__(self, model=""):
        super(DBHandler, self).__init__()
        self.module_path = model.rsplit('.', 1)[0]
        self.model_name = model.rsplit('.', 1)[-1]
        self.model = None

    def emit(self, record):
        try:
            self.model = getattr(__import__(self.module_path, fromlist=[self.model_name]), self.model_name)
        except ModuleNotFoundError as e:
            raise e

        data = {}
        for field in self.model._meta.get_fields():
            if hasattr(record, field.name):
                data[field.name] = getattr(record, field.name)
            elif field.name == 'level':
                data[field.name] = getattr(record, 'levelname')
            elif field.name == 'function':
                data[field.name] = getattr(record, 'funcName')
            elif field.name == 'message':
                data[field.name] = getattr(record, 'msg')

        try:
            self.model.objects.using('logging').create(**data)
        except IntegrityError as e:
            raise e
