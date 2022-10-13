import pandas as pd
import os
import requests
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup
from functools import wraps
from concurrent.futures import as_completed, ThreadPoolExecutor

def authentication(func):
    @wraps(func)
    def run_checks(self, *args, **kwargs):
        if self.cookie == None:
            print("[!] Need Authentication:\nYou must provide the Trailforks class with a valid cookie (trailforks_cookie=<cookie>)")
            exit(1)
        return func(self, *args, **kwargs) 
    return run_checks
        

class Trailforks:
    def __init__(self, region=None, username=None, trailforks_cookie=None):
        self.name = "trailforks"
        self.region = region
        self.username = username
        self.cookie = trailforks_cookie

    def login(self) -> dict:

        payload = {
            "ripformname": "loginform",
            "formpage": "/login/#loginform",
            "fieldstack[0]": "source",
            "source-alpha": "trailforks",
            "fieldstack[1]": "redirect",
            "redirect-textbasic": "https://www.trailforks.com/profile/mnmtb/",
            "fieldstack[2]": "username",
            "username-login-loginlen": "faust.joshua@gmail.com",
            "fieldstack[3]": "password",
            "password-password-lt200": "REDACTED--",
            "fieldstack[4]": "rememberme",
            "rememberme": "",
            "fieldstack[5]": "logoutother",
            "submitbutton['Login']": "Login",
            "buttondest['Login']": "https://www.trailforks.com/x_login_form/",
            "iebug": "1",
            "formhash": "+t9UzozSkiKVu3yg/RbklLzMiIMMM5ZugdjIAErjjuyePSeHzcyU1tI+5FY6qwp4bMrODuKcbiFezpOKI1CHfk23otrHiAsNEexbV1FxEKHi+4KJFkqzQeIMYFkLyHdDpx+cm+5biT8RmOPLk9XFjGfLhBwzICeq8h/88ppUDmvt5swhphHaOJI="
        }

        r = requests.post("https://trailforks.com/wosFormCheck.php", data=payload)
        return r.text

    def check_region(self) -> None:
        """
        Some requests require authentication (login) and you need to present a valid
        cookie to trailforks before you can do anything.
        """
        if self.region == None:
            print("[!] Need Region:\nYou must provide a valid Region (region=<region_name>)")
            exit(1)  

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
        function attempts to normalize them into miles (int)

        Args:
            distance (str): string of distance, 1456 ft

        Returns:
            float: number of miles
        """
        try:
            if "ft" in distance:
                feet_int = int(distance.split(" ")[0].replace(",",""))
                mi = 0.000189394
                return feet_int * mi
            else:
                return float(distance.split(" ")[0])
        except Exception as e:
            return 0
