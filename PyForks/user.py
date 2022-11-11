import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyForks.trailforks import Trailforks, authentication
import re


class User(Trailforks):
    def get_user_info(self, user: str) -> dict:
        """
        Obtains user information via the user profile page
        and recent ridelogs

        Args:
            user (str): A Trailforks username

        Returns:
            dict: {username, profile, <location...>, recent rides}
        """
        user = user.split(" ")[0]
        user_data = {
            "username": user,
            "profile_link": f"https://www.trailforks.com/profile/{user}",
            "city": None,
            "state": None,
            "country": None,
            "recent_ride_locations": self.__get_user_recent_rides(user),
        }
        (
            user_data["city"],
            user_data["state"],
            user_data["country"],
        ) = self.__get_user_city_state_country(user)

        (
            user_data["admin_region"],
            user_data["is_regional_admin"],
        ) = self.is_regional_admin(user)
        return user_data

    @authentication
    def rescan_ridelogs_for_badges(self, ride_ids: list) -> bool:
        """
        If you add a new badge or new badges have been added that your
        old rides are currently not counting for, you can rescan them to
        and receive the credit deserved.

        Args:
            ride_ids (list): A list of ride IDs obtained via user ridelogs

        Returns:
            bool: True:Success;False:Failed
        """
        try:
            for id in ride_ids:
                uri = f"https://www.trailforks.com/ridelog/view/{id.strip()}/rescanbadges/"
                headers = {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
                }
                r = self.trailforks_session.get(uri)
                if "<title>Error</title>" in r.text:
                    raise Exception("Invalid Ride ID and/or Unauthorized")
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_ridelogs_all(self, user: str) -> pd.DataFrame:
        """
        Scrape all of the users ridelogs and throw that into a pandas
        dataframe.

        Args:
            user (str): A Trailforks username

        Returns:
            pd.DataFrame: Pandas dataframe of all rides ever subject to the user
        """
        uri = f"https://www.trailforks.com/profile/{self.uri_encode(user)}/ridelog/?sort=l.timestamp&activitytype=1&year=0&bikeid=0&raceid=0"
        r = requests.get(uri)
        df = pd.read_html(r.text)[0]
        df["ridelog_link"] = self.__get_ridelog_links(r.text)
        df["ride_id"] = self._parse_ride_ids(df.ridelog_link.to_list())
        return df

    def __get_ridelog_links(self, html_data: str) -> list:
        """
        Parses the ridelog links from the users ridelog data

        Args:
            html_data (str): HTML of the users ridelog page

        Returns:
            list: List of unique ridelog links
        """
        soup = BeautifulSoup(html_data, "html.parser")
        table = soup.find("table")

        links = set()
        for tr in table.findAll("tr"):
            trs = tr.findAll("td")
            for each in trs:
                try:
                    link = each.find("a")["href"]
                    if "ridelog/view" in link and "achievements" not in link:
                        links.add(link)
                except:
                    pass
        return list(links)

    def _parse_ride_ids(self, ridelog_links: list) -> list:
        """
        Parses out the ridelog IDs from a ridelog link

        Args:
            ridelog_links (list): A list of ridelog links

        Returns:
            list: List of unique ride IDs
        """

        rex = re.compile(r"view\/(\d{8})/$")
        ids = []
        for link in ridelog_links:
            try:
                ids.append(rex.search(link).group(1))
            except AttributeError as e:
                pass
        return ids

    def __get_user_city_state_country(self, user: str) -> tuple:
        """
        From HTML Source of the users profile page, parse out the
        city, state, and country attributes.

        Args:
            user (str): A Trailforks Username

        Returns:
            tuple: (city, state, country)
        """

        user_uri = f"https://www.trailforks.com/profile/{self.uri_encode(user)}"
        page = requests.get(user_uri)
        soup = BeautifulSoup(page.text, "html.parser")

        city = "unknown"
        state = "unknown"
        country = "unknown"
        # get the users city and state
        try:
            location = soup.find("li", class_="location").getText()
            city, state = location.strip().split(",")
            city = city.strip()
            state = state.strip()
            country = "USA"
        except AttributeError as e:
            pass
        except ValueError as e:
            try:
                city, state, country = location.strip().split(",")
                city = city.strip()
                state = "unknown"
                country = country.strip()
            except Exception as e:
                state = location.strip()

        return (city, state, country)

    def __get_user_recent_rides(self, user: str) -> list:
        """
        Obtain a list of the most recent rides by region

        Args:
            user (str): A Trailforks Username

        Returns:
            list: List of unique regions
        """
        # get the users most recent (current year) riding locations
        try:
            activity_uri = f"https://www.trailforks.com/profile/{self.uri_encode(user)}/ridelog/?sort=l.timestamp&activitytype=1&year=0&bikeid=0"
            activity_df = pd.read_html(activity_uri)[0]
            activity_df = activity_df.fillna("")
            recent_ride_locations = activity_df.location.unique().tolist()
            recent_ride_locations.remove("")
        except ValueError as e:
            recent_ride_locations = []

        return recent_ride_locations

    @authentication
    def get_user_gear(self, user: str) -> list:
        """
        Get the users bike/gear they're using

        Args:
            user (str): A Trailforks User

        Returns:
            list: a list of tuples [(brand, model), (brand, model)]
        """
        uri = f"https://www.trailforks.com/profile/{self.uri_encode(user)}/bikes/"
        r = self.trailforks_session.get(uri)
        try:
            df = pd.read_html(r.text)[0]
            df = df[df["model"].notna()]
            user_gear = list(zip(df.brand, df.model))
        except ValueError as e:
            user_gear = []
        return user_gear

    def is_regional_admin(self, user: str) -> tuple:
        """
        Determines if a user is a regional admin and returns
        the region they're an admin of (link and name)

        Args:
            user (str): Trailforks username

        Returns:
            tuple: ({region_link, region_name}, is_admin bool)
        """
        uri = f"https://www.trailforks.com/profile/{self.uri_encode(user)}/"
        r = requests.get(uri)
        try:
            soup = BeautifulSoup(r.text, "html.parser")
            col_5 = soup.find("div", {"class", "col-5"})
            region_link, region_name = re.search(
                r'Admin</h4>.*<a href="(https.*)">([aA0-zZ9]+)</a>',
                str(col_5),
                re.DOTALL | re.MULTILINE,
            ).groups()
            return ({"region_link": region_link, "region_name": region_name}, True)
        except AttributeError:
            return ({"region_link": "", "region_name": ""}, False)
