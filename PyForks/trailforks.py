import sys
import requests
import urllib.parse
import logging
import json
#import pandas as pd
import PyForks.exceptions
import pkg_resources
from functools import wraps


def authentication(func):
    """
    Authentication Decorator for functions that need a valid Trailforks
    user session to complete a task such as downloading CSV reports

    Args:
        func (_type_): callable function

    Returns:
        _type_: original function
    """

    @wraps(func)
    def run_checks(self, *args, **kwargs):
        if self.app_id == None or self.app_secret == None:
            print(
                f"[!] Need Authentication:\nYou must provide app_id= and app_secret=\n"
            )
            exit(1)
        return func(self, *args, **kwargs)

    return run_checks


class Trailforks:
    def __init__(self, app_id=None, app_secret=None, debug=False):
        self.base_uri = "https://www.trailforks.com/api/1"
        self.__init_logger()
        self._logger = logging.getLogger("PyForks")
        self.name = "trailforks"
        self.app_id = app_id
        self.app_secret = app_secret
        self.trailforks_session = requests.Session()
        self.region_data_file = pkg_resources.resource_filename("PyForks", "data/region_data.parquet")
        #self.regions_df = pd.read_parquet(self.region_data_file, engine="pyarrow")
        self.debug = debug

        if self.debug:
            logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


    def _get(self, endpoint: str,  params:dict) -> requests.Response:
        """
        Performs a GET request to the Trailforks API

        Args:
            params (dict): Dictionary of parameters to pass to the API

        Returns:
            json: JSON response from the Trailforks API
        """
        try:
            auth_params = {"app_id": self.app_id, "app_secret": self.app_secret}
            params.update(auth_params)
            
            r = self.trailforks_session.get(endpoint, params=params)
            return r
        except Exception as e:
            print(f"[!] ERROR: {e}")

    def _post(self, endpoint: str,  params:dict) -> requests.Response:
        """
        Performs a POST request to the Trailforks API

        Args:
            params (dict): Dictionary of parameters to pass to the API

        Returns:
            json: JSON response from the Trailforks API
        """
        try:
            auth_params = {"app_id": self.app_id, "app_secret": self.app_secret}
            params.update(auth_params)
            r = self.trailforks_session.post(endpoint, params=params)
            return r
        except Exception as e:
            print(f"[!] ERROR: {e}")

    def uri_encode(self, string: str) -> str:
        """
        URIEncode things that need encoding

        Args:
            string (str): string to encode

        Returns:
            str: encoded string
        """
        return urllib.parse.quote(string)

    def distance_string_to_miles_float(self, distance: str) -> float:
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
            self._logger.error(f"distance casting failed;ERROR:{e}")
            return 0

    def feet_to_miles(self, feet: int) -> float:
        """
        Translate feet into miles

        Args:
            feet (int): feet as a integet

        Returns:
            float: miles as a float
        """
        feet = int(feet.replace(",", "").strip())
        mi = 0.000189394
        return feet * mi
    
    def meters_to_miles(self, meters: float) -> float:
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

    def has_numbers(self, data: str) -> bool:
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

    def make_trailforks_request(self, uri: str) -> json:
        """
        Makes a request give a URI

        Args:
            uri (str): URI String

        Returns:
            json: Trailforks API response JSON Data object
        """
        try:
            r = self.trailforks_session.get(uri)
            url_json = r.json()
            self._handle_api_error(url_json)
            self._handle_status_code(r.status_code, url_json["message"])
            url_json_data = url_json["data"]
            return url_json_data
        except Exception as e:
            raise PyForks.exceptions.TrailforksAPIException(
                msg="[!] ERROR: Bad API App or Secret Key"
            )

    def _handle_status_code(self, status_code: int, message: str) -> None:
        """
        Handle unauthenticated or incorrect permissions errors for HTTP requests

        Args:
            status_code (int): HTTP Status Code
            message (str): Trailforks API Message

        Raises:
            PyForks.exceptions.RegionLockedAPI: 401 is usually tied to a failure in permissions for a token
        """
        if status_code == 401:
            raise PyForks.exceptions.RegionLockedAPI(
                msg=f"[!] Error: {message}"
            )
        
    def _handle_api_error(self, api_response: json) -> None:
        """
        The Trailforks API gives us an indication if a request has been made that
        resulted in an error. This function handles that notification to a user if
        an error state is seen

        Args:
            api_response (json): API Response JSON object

        Raises:
            PyForks.exceptions.TrailforksAPIException: _description_
        """
        if api_response['error'] != 0:
            raise PyForks.exceptions.TrailforksAPIException(
                msg=f"[!] API Error: {api_response['message']}"
            )
        
    def __init_logger(self) -> None:
        """
        Initializes the PyForks Logging facility
        """
        logger = logging.getLogger("PyForks")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
