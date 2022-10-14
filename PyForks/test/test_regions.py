from PyForks.trailforks_region import TrailforksRegion, Trailforks


def test_nonexistant_region():
    region = TrailforksRegion(region="bullcrap_region")
    assert region.is_valid_region() == False

def test_existant_region():
    region = TrailforksRegion(region="buck-hill-52165")
    assert region.is_valid_region() == True

def test_trailforks_login_fail():
    region = TrailforksRegion(region="buck-hill-52165", username="mnmtb", password="not_my_password")
    login = region.login()
    assert login == False