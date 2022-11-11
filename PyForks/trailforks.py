import os
import requests
import pickle
import urllib.parse
from bs4 import BeautifulSoup
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
        if not self.authenticated:
            print(
                f"[!] Need Authentication:\nYou must provide username= and password=\n+ {self._login_error}"
            )
            exit(1)
        return func(self, *args, **kwargs)

    return run_checks

def requires_user_pass(func):
    """
    User Pass requirement decorator

    Args:
        func (_type_): callable function

    Returns:
        _type_: original function
    """

    @wraps(func)
    def run_checks(self, *args, **kwargs):
        if None in [self.username, self.password]:
            print(
                f"[!] You must provide username= and password=\n+ {self._login_error}"
            )
            exit(1)
        return func(self, *args, **kwargs)

    return run_checks


class Trailforks:
    def __init__(self, username=None, password=None):
        self.name = "trailforks"
        self.username = username
        self.password = password
        self.trailforks_session = None
        self.authenticated = False
        self._login_page_title = None
        self._login_error = None
        self.__cookie_cache = f"{os.getcwd()}/.cookie"

    @requires_user_pass
    def login(self) -> bool:
        """
        Login to Trailforks with a username and password in order to conduct
        privileged (user based) operations such as downloading content or
        viewing non-public information.

        Returns:
            bool: True:successful login;False:failed to login
        """
        trailforks_session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        }
        t = trailforks_session.get(
            "https://www.trailforks.com/login/#loginform",
            headers=headers,
            allow_redirects=True,
        )
        form_hash = self.__get_trailforks_formhash(t.text)
        users_homepage = (
            f"https://www.trailforks.com/profile/{self.uri_encode(self.username)}/"
        )

        payload = {
            "ripformname": "loginform",
            "formpage": "/login/#loginform",
            "fieldstack[0]": "source",
            "source-alpha": "trailforks",
            "fieldstack[1]": "redirect",
            "redirect-textbasic": users_homepage,
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
            "formhash": form_hash,
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
            "Sec-GPC": "1",
        }

        if os.path.exists(self.__cookie_cache):
            cookies = self.__load_cookie()
            try:
                trailforks_session.cookies.update(cookies)
                t = trailforks_session.get(users_homepage, allow_redirects=True)
            except TypeError as e:
                print("[!] Bad cookie file. Please delete the .cookie file and try again")
                return False
        else:
            t = trailforks_session.post(
                "https://www.trailforks.com/wosFormCheck.php",
                data=payload,
                headers=headers_login,
                allow_redirects=True,
            )

        self._login_page_title = self.__get_trailforks_page_title(t.text)

        if self.username in self._login_page_title:
            self.trailforks_session = trailforks_session
            self.authenticated = True
            self.__cache_cookie(trailforks_session.cookies)
            return True

        self._login_error = self.__get_rip_error(t.text)
        return False

    def __load_cookie(self) -> requests.cookies.RequestsCookieJar:
        """
        Load existing Trailforks cookies for authentication

        Returns:
            requests.Session.cookies: Requests Session Cookies object
        """
        try:
            with open(self.__cookie_cache, "rb") as f:
                cookies = pickle.load(f)
            return cookies
        except pickle.UnpicklingError as e:
            return None

    def __cache_cookie(self, cookies: requests.cookies.RequestsCookieJar) -> bool:
        """
        Cache a cookie incase the user wants to run other scripts.
        This way we will not get a too many login attempts exception
        from Trailforks.

        Args:
            cookies (requests.Session.cookies): Requests Session Cookie object

        Returns:
            bool: True:cookie was saved;False:cookie was not saved
        """
        try:
            with open(self.__cookie_cache, "wb") as f:
                pickle.dump(cookies, f)
            return True
        except Exception as e:
            print(f"[!] Error Saving Cookie: {e}")
            return False

    def __get_rip_error(self, html: str) -> str:
        """
        Get the login error code if we failed to login

        Args:
            html (str): Raw login HTML attempt

        Returns:
            str: string error code (i.e., too many login attempts)
        """
        soup = BeautifulSoup(html, "html.parser")
        rip_error = soup.find("div", {"class": "ripError"}).text
        return rip_error

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
        form_hash = soup.find("input", {"name": "formhash"}).get("value")
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
        title_tag = soup.find("title")
        return title_tag.string

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
        miles_strings = ["mi", "miles"]
        distance = distance.replace('"', "")
        try:
            if any(x in distance for x in feet_strings):
                distance_int = int(distance.split(" ")[0].replace(",", ""))
                mi = 0.000189394
                return distance_int * mi
            elif any(x in distance for x in feet_strings):
                distance_int = int(distance.split(" ")[0].replace(",", ""))
                return distance_int
            else:
                return float(distance.split(" ")[0])
        except Exception as e:
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
