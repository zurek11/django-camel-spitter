import logging
import pytest
from tests.models import ExtendedLogEntry


@pytest.mark.django_db
class TestExtendedLogger:
    ERROR_MESSAGE = 'TEST_EXTENDED_LOGGER'

    def test_basic_logger(self):
        handler = logging.getLogger('logger').handlers[0]
        handler.model_name = 'ExtendedLogEntry'
        handler.module_path = 'tests.models'

        logging.getLogger('logger').error(self.ERROR_MESSAGE, extra={
            'special': 'Foo', 'user': 'Bar', 'amount': 20
        })
        logged_information = ExtendedLogEntry.objects.get(special='Foo')

        assert logged_information.message == self.ERROR_MESSAGE
