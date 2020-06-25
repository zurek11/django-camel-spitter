from logging import Filter
from django.utils.translation import gettext as _


class DBFilter(Filter):
    def filter(self, record):
        if not hasattr(record, 'msg'):
            record.msg = _('Unknown message.')

        return True
