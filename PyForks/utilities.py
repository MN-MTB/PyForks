import logging 

def distance_string_to_miles_float(distance: str) -> float:
    """
    Trailforks report data has mixed distance values, this
    function attempts to normalize them into miles (float)

    Args:
        distance (str): string of distance, 1456 ft, 2.3mi

    Returns:
        float: number of miles
    """
    feet_strings = ["ft", "feet"]
    distance = distance.replace('"', "")
    try:
        if any(x in distance for x in feet_strings):
            distance_int = int(distance.split(" ")[0].replace(",", ""))
            mi = 0.000189394
            return distance_int * mi
        else:
            return float(distance.split(" ")[0])
    except Exception as e:
        logging.error(f"distance casting failed;ERROR:{e}")
        return 0

def feet_to_miles(feet: int) -> float:
    """
    Translate feet into miles

    Args:
        feet (int): feet as a integer

    Returns:
        float: miles as a float
    """
    if isinstance(feet, str):
        feet = int(feet.replace(",", "").strip())
    mi = 0.000189394
    return feet * mi

def meters_to_miles(meters: float) -> float:
    """
    Translates meters to miles since the trailforks uses
    metric measurements for their API.

    Args:
        meters (int): Total Meters

    Returns:
        float: Total Miles
    """
    meters = float(meters)
    miles = meters * 0.00062137
    return miles

def has_numbers(data: str) -> bool:
    """
    Determines if there are numbers in a string

    Args:
        data (str): String to check

    Returns:
        bool: True: numbers exist; False: numbers do not exist
    """
    try:
        check = any(char.isdigit() for char in data)
        return check
    except TypeError:
        return True