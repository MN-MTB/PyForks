from PyForks.trailforks_region import TrailforksRegion, Trailforks


def test_login():
    t = Trailforks()
    print(t.login())

def test_nonexistant_region():
    region = TrailforksRegion(region="bullcrap_region")
    assert region.is_valid_region() == False

def test_existant_region():
    region = TrailforksRegion(region="buck-hill-52165")
    assert region.is_valid_region() == True

def test_download_region_ridelogs():
    region = TrailforksRegion(region="buck-hill-52165")
    region.download_all_region_rides("52165")