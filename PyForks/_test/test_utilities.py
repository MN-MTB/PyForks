from PyForks.utilities import distance_string_to_miles_float, feet_to_miles, meters_to_miles, has_numbers

def test_distance_string_to_miles_float():
    assert distance_string_to_miles_float("1456 ft") == 0.275757664
    assert distance_string_to_miles_float('2,500 ft') == 0.47348500000000004

def test_feet_to_miles():
    assert feet_to_miles("1456") == 0.275757664
    assert feet_to_miles("2,500") == 0.47348500000000004

def test_meters_to_miles():
    assert meters_to_miles(1456) == 0.90471472
    assert meters_to_miles(2500) == 1.553425

def test_has_numbers():
    string_num = "This is a string with numbers 1234567890"
    string_no_num = "This is a string without numbers"
    assert has_numbers(string_num) == True
    assert has_numbers(string_no_num) == False
