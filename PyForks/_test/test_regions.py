from PyForks.trailforks_region import TrailforksRegion, Trailforks


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