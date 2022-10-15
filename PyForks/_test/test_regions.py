from PyForks.trailforks_region import TrailforksRegion, Trailforks
import pytest

def test_nonexistant_region():
    region = TrailforksRegion()
    assert region.is_valid_region(region="bullcrap_region") == False

def test_existant_region():
    region = TrailforksRegion()
    assert region.is_valid_region(region="buck-hill-52165") == True

def test_trailforks_login_fail():
    region = TrailforksRegion(username="mnmtb", password="not_my_password")
    login = region.login()
    assert login == False

def test_check_bad_region():
    region = TrailforksRegion()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        region.check_region("fake_004957856934")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_check_good_region():
    region = TrailforksRegion()
    check = region.check_region("lebanon-hills")
    assert check == True

def test_get_region_info():
    region = TrailforksRegion()
    check = region._get_region_info("lebanon-hills")
    assert isinstance(check, dict)

"""
def test_ridelogcount_download_lowpriv_user():
    region = TrailforksRegion(username="", password="")
    region.login()
    download_result = region.download_region_ridecounts("west-lake-marion-park")
    assert download_result == True

def test_trails_download_lowpriv_user():
    region = TrailforksRegion(username="", password="")
    region.login()
    download_result = region.download_all_region_trails("west-lake-marion-park", "20367")
    assert download_result == False

def test_ridelogs_download_lowpriv_user():
    region = TrailforksRegion(username="", password="")
    region.login()
    download_result = region.download_all_region_ridelogs("west-lake-marion-park")
    assert download_result == True
"""