from PyForks import Events
import pytest
import os

class TestEvents:
    @pytest.fixture
    def events(self):
        APP_ID = os.getenv("APP_ID")
        APP_SECRET = os.getenv("APP_SECRET")
        return Events(app_id=APP_ID, app_secret=APP_SECRET)

    def test_get_event(self, events):
        response = events.get_event(123)
        assert isinstance(response, dict)

    def test_get_events(self, events):
        response = events.get_events()
        assert isinstance(response, dict)