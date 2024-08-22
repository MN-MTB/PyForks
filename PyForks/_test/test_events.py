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
        event_id = 11403
        response = events.get_event(11403)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and response['data']['id'] == str(event_id)

    def test_get_events(self, events):
        args = {"filter": "rid::3203"} # Minnesota Region
        response = events.get_events(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response 
