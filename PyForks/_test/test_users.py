from PyForks.user import User
import pandas as pd
import pytest
import PyForks.exceptions


def test_bad_username():
    tf_user = User()

    with pytest.raises(PyForks.exceptions.InvalidUser) as pytest_wrapped_e:
        user_data = tf_user.get_user_info("09846759345fdsadfa")

    assert pytest_wrapped_e.type == PyForks.exceptions.InvalidUser


def test_bad_ride_links():
    ride_links = [
        "https://www.trailforks.com/ridelog/view/41911060/",
        "https://www.trailforks.com/ridelog/view/060/asdfasdfasdf",
        "https://www.trailforks.com/ridelog/view/4191ffffffffff0/",
        "https://www.trailforks.com/ri---d",
    ]
    tf_user = User()
    ride_ids = tf_user._parse_ride_ids(ride_links)
    assert ride_ids == ["41911060"]


def test_is_admin():
    tf_user = User()
    region, is_admin = tf_user.is_regional_admin("mnmtb")
    assert is_admin == True


def test_is_admin_fail():
    tf_user = User()
    region, is_admin = tf_user.is_regional_admin("asdfdfsafsdf")
    assert is_admin == False


def test_badge_rescan_bad_ids():
    bad_ride_ids = ["1"]
    tf_user = User(username="apress001", password="FakePassword123")
    tf_user.login()
    check = tf_user.rescan_ridelogs_for_badges(bad_ride_ids)
    assert check == False


def test_get_user_gear():
    tf_user = User(username="apress001", password="FakePassword123")
    tf_user.login()
    check = tf_user.get_user_gear("mnmtb")
    assert check == [('Orbea', 'Occam H20 Eagle')]


def test_get_user_gear_no_gear():
    tf_user = User(username="apress001", password="FakePassword123")
    tf_user.login()
    check = tf_user.get_user_gear("apress001")
    assert check == []


def test_badge_rescan_good_id():
    id = ["46233241"]
    tf_user = User(username="apress001", password="FakePassword123")
    tf_user.login()
    check = tf_user.rescan_ridelogs_for_badges(id)
    assert check == True


def test_get_user_ridelogs():
    tf_user = User()
    rides_df = tf_user.get_user_ridelogs_all("mnmtb")
    assert isinstance(rides_df, pd.DataFrame) and len(rides_df.index) > 5


def test_get_user_info():
    tf_user = User()
    users = ["bcpov","canadaka", "apress001", "mnmtb"]
    for user in users:
        user_data = tf_user.get_user_info(user)
    assert (
        (isinstance(user_data, dict))
        and user_data["city"] == "Lakeville"
        and user_data["state"] == "Minnesota"
    )
