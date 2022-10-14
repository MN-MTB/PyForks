from PyForks.trailforks_user import TrailforksUser


def test_bad_username():
    tf_user = TrailforksUser()
    user_data = tf_user.get_user_info("09846759345fdsadfa")
    expected = {
        'username': '09846759345fdsadfa', 
        'profile_link': 'https://www.trailforks.com/profile/09846759345fdsadfa', 
        'city': 'unknown', 
        'state': 'unknown', 
        'country': 'unknown', 
        'recent_ride_locations': []
        }
    assert user_data == expected


def test_good_username():
    tf_user = TrailforksUser()
    user_data = tf_user.get_user_info("mnmtb")
    expected = {
        'username': 'mnmtb', 
        'profile_link': 'https://www.trailforks.com/profile/mnmtb', 
        'city': 'Lakeville', 
        'state': 'Minnesota', 
        'country': 'USA', 
        'recent_ride_locations': ['Murphy-Hanrehan Park', 'Lebanon Hills', 'West Lake Marion Park', 'Spirit Mountain Bike Park', '', 'Battle Creek', 'Cottage Grove Bike Park', 'Lakeville']
        }
    assert user_data == expected


def test_bad_ride_links():
    ride_links = [
        "https://www.trailforks.com/ridelog/view/41911060/",
        "https://www.trailforks.com/ridelog/view/060/asdfasdfasdf",
        "https://www.trailforks.com/ridelog/view/4191ffffffffff0/",
        "https://www.trailforks.com/ri---d"
    ]
    tf_user = TrailforksUser()
    ride_ids = tf_user._parse_ride_ids(ride_links)
    assert ride_ids == ['41911060']

