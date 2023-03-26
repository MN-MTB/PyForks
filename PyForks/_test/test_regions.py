from PyForks import Region
import PyForks.exceptions
import pytest
import pandas as pd
import os

APP_ID = os.environ("APP_ID")
APP_SECRET = os.environ("APP_SECRET")

def test_nonexistant_region():
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    assert region.is_valid_region("bullcrap_region") == False


def test_existant_region():
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    assert region.is_valid_region("buck-hill-52165") == True


def test_check_bad_region():
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    with pytest.raises(PyForks.exceptions.InvalidRegion) as pytest_wrapped_e:
        region.check_region("fake_004957856934")
    assert pytest_wrapped_e.type == PyForks.exceptions.InvalidRegion


def test_check_good_region():
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    check = region.check_region("lebanon-hills")
    assert check == True


def test_get_region_info():
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    check = region.get_region_info("lebanon-hills")
    assert isinstance(check, dict)


def test_ridelogcount_download_auth_fail():
    region = Region()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        region.get_region_ridecounts("west-lake-marion-park")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_trails_download_auth_fail():
    region = Region()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        region.get_all_region_trails("west-lake-marion-park")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ridelogs_download_auth_fail():
    region = Region()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        region.get_all_region_ridelogs("west-lake-marion-park")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ridelogcount_download():
    """
    A low-priv user should be able to download region ridecounts
    """
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    download_result = region.get_region_ridecounts("west-lake-marion-park")
    assert isinstance(download_result, pd.DataFrame) and len(download_result.index) > 5


def test_ridelogs_download():
    """
    A low-priv user (non-admin) should be able to download the ridecounts for
    a region.
    """
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    download_result = region.get_all_region_ridelogs("west-lake-marion-park")

    assert isinstance(download_result, pd.DataFrame) and len(download_result.index) > 5

def test_ridelogs_download_small_pages():
    """
    A low-priv user (non-admin) should be able to download the ridecounts for
    a region.
    """
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    download_result = region.get_all_region_ridelogs("west-lake-marion-park", pages=1)

    assert isinstance(download_result, pd.DataFrame) and len(download_result.index) > 5


def test_region_get_info():
    region = Region(app_id=APP_ID, app_secret=APP_SECRET)
    info = region.get_region_info("battle-creek-5538")
    expected = {
            "total_ridelogs": 4499,
            "unique_riders": 1155,
            "trails_ridden": 76745,
            "average_trails_per_ride": 151,
            "total_trails": "26",
            "trails_(view_details)": "26",
            "trails_mountain_bike": "26",
            "trails_hike": "24",
            "trails_trail_running": "24",
            "total_distance": "10 miles",
            "total_descent": "1,522 ft",
            "total_vertical": "271 ft",
            "highest_trailhead": "992 ft",
            "reports": "528",
            "photos": "21",
            "ridden_counter": "13,882",
            "country": "United States",
            "state_province": "Minnesota",
            "city": "St. Paul"
        }
    
    assert (
        expected["total_trails"] == info["total_trails"] 
        and expected["country"] == info["country"]
        and expected["state_province"] == info["state_province"]
        and expected["city"] == info["city"]
    )
