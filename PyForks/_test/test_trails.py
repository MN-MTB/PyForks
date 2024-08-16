from PyForks import Trails
import pytest
import os

class TestTrails:
    @pytest.fixture
    def trails(self):
        if os.name in ['nt']:
            print(os.name)
            from configparser import ConfigParser
            parser = ConfigParser()
            parser.read("./PyForks/_test/secrets.ini")
            APP_ID = parser['trailforks']['app_id']
            APP_SECRET = parser['trailforks']['app_secret']
        else:
            print(os.name)
            APP_ID = os.getenv("APP_ID")
            APP_SECRET = os.getenv("APP_SECRET")
        return Trails(app_id=APP_ID, app_secret=APP_SECRET)

    def test_get_map_trails(self, trails):
        response = trails.get_map_trails()
        assert isinstance(response, dict)

    def test_get_trail(self, trails):
        response = trails.get_trail(123)
        assert isinstance(response, dict)

    def test_get_trail_status(self, trails):
        response = trails.get_trail_status(123456)
        assert isinstance(response, dict)

    def test_get_trails(self, trails):
        response = trails.get_trails()
        assert isinstance(response, dict)

    def test_post_waypoint(self, trails):
        response = trails.post_waypoint(1, 123.456, 78.9)
        assert isinstance(response, dict)

    def test_post_report(self, trails):
        response = trails.post_report(123, 1)
        assert isinstance(response, dict)

    def test_get_reports(self, trails):
        response = trails.get_reports()
        assert isinstance(response, dict)