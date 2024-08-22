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
        wlmt_table_jump_poi = 97398
        response = regions.get_poi(wlmt_table_jump_poi)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and response['data']['id'] == str(wlmt_table_jump_poi)

    def test_get_region(self, regions):
        west_lake_marion_id = 20367
        response = regions.get_region(west_lake_marion_id)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and response['data']['rid'] == west_lake_marion_id

    def test_get_region_status(self, regions):
        from datetime import datetime
        import time
        west_lake_marion_id = 20367
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d")
        timestamp = int(time.mktime(date_obj.timetuple()))
        args = {"rids": west_lake_marion_id}
        response = regions.get_region_status(timestamp, **args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response

    def test_get_regions(self, regions):
        args = {"rows": 40}
        response = regions.get_regions(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and len(response['data']) == 40

    def test_get_ridelogs(self, regions):
        west_lake_marion_id = 20367
        args = {"rid": west_lake_marion_id, "rows": 20}
        response = regions.get_ridelogs(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and len(response['data']) == 20

    # def test_get_rideplan(self, regions):
    #     rideplan_id = 123
    #     response = regions.get_rideplan(123)
    #     assert isinstance(response, dict)

    # def test_get_rideplans(self, regions):
    #     response = regions.get_rideplans()
    #     assert isinstance(response, dict)

    def test_get_route(self, regions):
        moab_route_id = 1250
        response = regions.get_route(moab_route_id)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and response['data']['id'] == moab_route_id

    def test_get_routes(self, regions):
        args = {"rows": 10, "filter": "featured::1"}
        response = regions.get_routes(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and len(response['data']) == 10

    def test_get_supporters(self, regions):
        args = {"filter": "rid::20367"}
        response = regions.get_supporters(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response and response['data'][0]['id'] == "12022"

    def test_get_videos(self, regions):
        args = {"filter": "rid::20367"}
        response = regions.get_videos(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response 

    def test_get_photos(self, regions):
        args = {"filter": "rid::20367"}
        response = regions.get_photos(**args)
        assert isinstance(response, dict) and response['error'] == 0 and "data" in response 
