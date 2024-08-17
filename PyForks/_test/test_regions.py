from PyForks import Regions
import os
import pytest

class TestRegions:
    @pytest.fixture
    def regions(self):
        APP_ID = os.getenv("APP_ID")
        APP_SECRET = os.getenv("APP_SECRET")
        return Regions(app_id=APP_ID, app_secret=APP_SECRET)

    def test_get_poi(self, regions):
        response = regions.get_poi(123)
        assert isinstance(response, dict)

    def test_get_region(self, regions):
        response = regions.get_region(123)
        assert isinstance(response, dict)

    def test_get_region_status(self, regions):
        response = regions.get_region_status(123456)
        assert isinstance(response, dict)

    def test_get_regions(self, regions):
        response = regions.get_regions()
        assert isinstance(response, dict)

    def test_get_ridelogs(self, regions):
        response = regions.get_ridelogs()
        assert isinstance(response, dict)

    def test_get_rideplan(self, regions):
        response = regions.get_rideplan(123)
        assert isinstance(response, dict)

    def test_get_rideplans(self, regions):
        response = regions.get_rideplans()
        assert isinstance(response, dict)

    def test_get_route(self, regions):
        response = regions.get_route(123)
        assert isinstance(response, dict)

    def test_get_routes(self, regions):
        response = regions.get_routes()
        assert isinstance(response, dict)

    def test_get_supporters(self, regions):
        response = regions.get_supporters()
        assert isinstance(response, dict)

    def test_get_videos(self, regions):
        response = regions.get_videos()
        assert isinstance(response, dict)

    def test_get_photos(self, regions):
        response = regions.get_photos()
        assert isinstance(response, dict)