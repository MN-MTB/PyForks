import pandas as pd
import os
import requests
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup
from functools import wraps
from concurrent.futures import as_completed, ThreadPoolExecutor

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
        if not self.authenticated:
            print("[!] Need Authentication:\nYou must provide the Trailforks class with a valid cookie (trailforks_cookie=<cookie>)")
            exit(1)
        return func(self, *args, **kwargs) 
    return run_checks
        

class Trailforks:
    def __init__(self, region=None, username=None, password=None):
        self.name = "trailforks"
        self.region = region
        self.username = username
        self.password = password
        self.trailforks_session = None
        self.authenticated = False

    def login(self) -> bool:
        """
        Login to Trailforks with a username and password in order to conduct
        privileged (user based) operations such as downloading content or 
        viewing non-public information.

        Returns:
            bool: True:successful login;False:failed to login
        """
        trailforks_session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}
        t = trailforks_session.get("https://www.trailforks.com/login/#loginform", headers=headers, allow_redirects=True)
        form_hash = self.__get_trailforks_formhash(t.text)

        payload = {
            "ripformname": "loginform",
            "formpage": "/login/#loginform",
            "fieldstack[0]": "source",
            "source-alpha": "trailforks",
            "fieldstack[1]": "redirect",
            "redirect-textbasic": "https://www.trailforks.com/profile/mnmtb/",
            "fieldstack[2]": "username",
            "username-login-loginlen": self.username,
            "fieldstack[3]": "password",
            "password-password-lt200": self.password,
            "fieldstack[4]": "rememberme",
            "rememberme": "",
            "fieldstack[5]": "logoutother",
            "submitbutton['Login']": "Login",
            "buttondest['Login']": "https://www.trailforks.com/x_login_form/",
            "iebug": "1",
            "formhash": form_hash
        }

        headers_login = {
            "Host": "www.trailforks.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "773",
            "Origin": "https://www.trailforks.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://www.trailforks.com/login/",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1"
        }

        t = trailforks_session.post("https://www.trailforks.com/wosFormCheck.php", data=payload, headers=headers_login, allow_redirects=True)
        if self.username in self.__get_trailforks_page_title(t.text):
            self.trailforks_session = trailforks_session
            self.authenticated = True
            return True
        return False

    def __get_trailforks_formhash(self, html: str) -> str:
        """
        Trailforms uses a login form hash value that dictates if a login
        action is valid as it's tied to either a previous login and/or a
        datetime object that serves as the expiration date. However, anytime
        a user vists the login page, a new formhash is generated and exists
        within the HTML. This function parses that hash out in order to
        successfully login to Trailforks without using Selenium

        Args:
            html (str): Raw HTML of the get request to the login page

        Returns:
            str: the formhash string
        """
        soup = BeautifulSoup(html, "html.parser")
        form_hash = soup.find('input', {'name': 'formhash'}).get('value')
        return form_hash

    def __get_trailforks_page_title(self, html: str) -> str:
        """
        Obtain the title of any page given its HTML content

        Args:
            html (str): Raw HTML

        Returns:
            str: Title string
        """
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find('title')
        return title_tag.string

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
