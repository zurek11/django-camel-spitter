import logging
import pytest
from tests.models import BasicLogEntry


@pytest.mark.django_db
class TestBasicLogger:
    ERROR_MESSAGE = 'TEST_BASIC_LOGGER'

    def test_basic_logger(self):
        handler = logging.getLogger('logger').handlers[0]
        handler.model_name = 'BasicLogEntry'
        handler.module_path = 'tests.models'

        logging.getLogger('logger').error(self.ERROR_MESSAGE)
        logged_information = BasicLogEntry.objects.get(message=self.ERROR_MESSAGE)

        assert logged_information.message == self.ERROR_MESSAGE
