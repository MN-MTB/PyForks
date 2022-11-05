from PyForks.user import User


def test_bad_username():
    tf_user = User()
    user_data = tf_user.get_user_info("09846759345fdsadfa")
    expected = {
        'admin_region': {'region_link': '', 'region_name': ''},
        'city': 'unknown',
        'country': 'unknown',
        'is_regional_admin': False,
        'profile_link': 'https://www.trailforks.com/profile/09846759345fdsadfa',
        'recent_ride_locations': [],
        'state': 'unknown',
        'username': '09846759345fdsadfa'
        }

    assert user_data == expected


def test_bad_ride_links():
    ride_links = [
        "https://www.trailforks.com/ridelog/view/41911060/",
        "https://www.trailforks.com/ridelog/view/060/asdfasdfasdf",
        "https://www.trailforks.com/ridelog/view/4191ffffffffff0/",
        "https://www.trailforks.com/ri---d"
    ]
    tf_user = User()
    ride_ids = tf_user._parse_ride_ids(ride_links)
    assert ride_ids == ['41911060']


def test_is_admin():
    tf_user = User()
    region, is_admin = tf_user.is_regional_admin("mnmtb")
    assert is_admin == True

def test_is_admin_fail():
    tf_user = User()
    region, is_admin = tf_user.is_regional_admin("asdfdfsafsdf")
    assert is_admin == False
