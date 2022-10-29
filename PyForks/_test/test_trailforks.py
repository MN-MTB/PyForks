from PyForks.trailforks_region import TrailforksRegion, Trailforks
import pytest

T = Trailforks()

def test_distance_cleaning():

    dirty_distances = ['3000 mi', "30 ft", "5,000 ft", "20 miles"]
    clean_distances = []
    expected_distances = [3000.0, 0.005681820000000001, 0.9469700000000001, 20.0]
    for distance in dirty_distances:
        clean_distances.append(T.distance_string_to_miles_float(distance))
    
    assert clean_distances == expected_distances