import pandas as pd
import os
import requests
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import as_completed, ThreadPoolExecutor
from src.trailforks import Trailforks
import re

class TrailforksUser(Trailforks):

    def get_user_info(self) -> dict:
        user = self.username.split(" ")[0]
        user_data = {
            "username": user,
            "profile_link": f"https://www.trailforks.com/profile/{user}",
            "city": None,
            "state": None,
            "country": None,
            "recent_ride_locations": self.__get_user_recent_rides(),
        }
        user_data["city"], user_data["state"], user_data["country"] = self.__get_user_city_state_country()
        return user_data


    def rescan_ridelogs_for_badges(self, ride_ids: list) -> bool:
        try:
            for id in ride_ids:
                uri = f"https://www.trailforks.com/ridelog/view/{id.strip()}/rescanbadges/"
                headers = {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
                }
                r = requests.get(
                    uri, 
                    allow_redirects=True, 
                    cookies=self.cookie, 
                    headers=headers
                    )
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_all_ridelogs(self) -> pd.DataFrame:
        uri = f"https://www.trailforks.com/profile/{self.uri_encode(self.username)}/ridelog/?sort=l.timestamp&activitytype=1&year=0&bikeid=0&raceid=0"
        r = requests.get(uri)
        df = pd.read_html(r.text)[0]
        with open("data.html", "w") as f:
            f.write(r.text)
        df["ridelog_link"] = self.__get_ridelog_links(r.text)
        df["ride_id"] = self.__parse_ride_ids(df.ridelog_link.to_list())
        return df

    def __get_ridelog_links(self, html_data: str) -> list:
        soup = BeautifulSoup(html_data, 'html.parser')
        table = soup.find('table')

        links = set()
        for tr in table.findAll("tr"):
            trs = tr.findAll("td")
            for each in trs:
                try:
                    link = each.find('a')['href']
                    if "ridelog/view" in link and "achievements" not in link:
                        links.add(link)
                except:
                    pass
        return list(links)


    def __parse_ride_ids(self, ridelog_links: list) -> str:
        rex = re.compile(r'view\/(\d{8})/$')
        ids = []
        for link in ridelog_links:
            ids.append(rex.search(link).group(1))
        return ids

    def __get_user_city_state_country(self) -> tuple:

        user_uri = f'https://www.trailforks.com/profile/{self.uri_encode(self.username)}'
        page = requests.get(user_uri)
        soup = BeautifulSoup(page.text, 'html.parser')

        # get the users city and state
        try:
            location = soup.find("li", class_="location").getText()
            city, state = location.strip().split(",")
            city = city.strip()
            state = state.strip()
            country = "USA"
        except AttributeError as e:
            city = "unknown"
            state = "unknown"
        except ValueError as e:
            try:
                city, state, country = location.strip().split(",")
                city = city.strip()
                state = "unknown"
                country = country.strip()
            except Exception as e:
                city = "unknown"
                state = location.strip()

        return (city, state, country)


    def __get_user_recent_rides(self) -> list:
        # get the users most recent (current year) riding locations
        try:
            activity_uri = f"https://www.trailforks.com/profile/{self.uri_encode(self.username)}/ridelog/?sort=l.timestamp&activitytype=1&year=0&bikeid=0"
            activity_df = pd.read_html(activity_uri)[0]
            recent_ride_locations = activity_df.location.unique().tolist()
        except ValueError as e:
            recent_ride_locations = []

        return recent_ride_locations

    def __get_user_gear(self) -> str:
        # get the users bikes/gear
        stats_uri = f"https://www.trailforks.com/profile/{self.uri_encode(self.username)}/ridelog/?sort=l.timestamp&year=0"
        page = requests.get(stats_uri)
        soup = BeautifulSoup(page.text, 'html.parser')

        try:
            ride_stats_divs = soup.find('div', id="myRidelogStats")
            divs = ride_stats_divs.find_all('div', class_="col-2")
            for div in divs:
                metric_name = div.find('div', class_="grey small").getText()
                metric_name = f"total_{metric_name.strip().replace(' ', '_').lower()}"
                metric = div.find('div', class_="large").getText()
                metric = metric.strip().lower()
                user_data = metric
        except AttributeError as e:
            pass
        
        return user_data









