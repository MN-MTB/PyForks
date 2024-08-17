from PyForks import Trails
import pytest
import os

class TestTrails:
    @pytest.fixture
    def trails(self):
        APP_ID = os.getenv("APP_ID")
        APP_SECRET = os.getenv("APP_SECRET")
        return Trails(app_id=APP_ID, app_secret=APP_SECRET)

    def test_get_map_trails(self, trails):
        trails_args = {"filter": "rid::20367"}
        response = trails.get_map_trails(**trails_args)
        print(response)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response

    def test_get_trail(self, trails):
        trail_id = 223516
        response = trails.get_trail(trail_id)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response

    def test_get_trail_status(self, trails):
        from datetime import datetime
        import time
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d")
        timestamp = int(time.mktime(date_obj.timetuple()))
        args = {"trailids": "223516"}
        response = trails.get_trail_status(timestamp, **args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response

    def test_get_trails(self, trails):
        args = {"filter": "rid::20367"}
        response = trails.get_trails(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and len(response['data']) > 20

    # def test_post_waypoint(self, trails):
    #     response = trails.post_waypoint(1, 123.456, 78.9)
    #     assert isinstance(response, dict)

    # def test_post_report(self, trails):
    #     response = trails.post_report(123, 1)
    #     assert isinstance(response, dict)

    def test_get_reports(self, trails):
        args = {"filter": "rid::20367"}
        response = trails.get_reports(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response