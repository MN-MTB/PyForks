from PyForks.trailforks import Trailforks
import pytest
import os

def test_distance_cleaning():
    tf = Trailforks()
    dirty_distances = ["3000 mi", "30 ft", "5,000 ft", "20 miles"]
    clean_distances = []
    expected_distances = [3000.0, 0.005681820000000001, 0.9469700000000001, 20.0]
    for distance in dirty_distances:
        clean_distances.append(tf.distance_string_to_miles_float(distance))

    assert clean_distances == expected_distances

def test_trailforks_login_fail():
    # remove any latent cookies to avoid valid logins since we check for cookies first
    if os.path.exists(".cookie"):
        os.remove(".cookie")
    tf = Trailforks(username="mnmtb", password="not_my_password")
    login = tf.login()
    assert login == False

def test_bad_cookie_load_fail():
    # remove any latent cookies to avoid valid logins since we check for cookies first
    if os.path.exists(".cookie"):
        os.remove(".cookie")
    
    with open(".cookie", "wb") as f:
        f.write(b'not a cookie brah')
    
    tf = Trailforks(username="apress001", password="FakePassword123")
    check = tf.login()
    assert check == False

def test_new_cookie_creation():
    # remove any latent cookies to avoid valid logins since we check for cookies first
    if os.path.exists(".cookie"):
        os.remove(".cookie")

    tf = Trailforks(username="apress001", password="FakePassword123")
    check = tf.login()
    assert os.path.exists(".cookie") == True

def test_login_with_cookie_only():
    tf = Trailforks()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tf.login()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1