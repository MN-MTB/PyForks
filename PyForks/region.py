import pandas as pd
import requests
import re
import json
import logging
from datetime import datetime
import io
import PyForks.exceptions
import calendar
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyForks.trailforks import Trailforks, authentication


class Region(Trailforks):
    def is_valid_region(self, region: str) -> bool:
        """
        Check to make sure a region name is a real region by
        making sure the page title is not Error

        Returns:
            bool: True:is an existing region;False:region does not exist.
        """  # noqa
        filter = self.uri_encode(f"alias::{region}")
        uri = f"https://www.trailforks.com/api/1/regions?filter={filter}&app_id={self.app_id}&app_secret={self.app_secret}"
        r = self.trailforks_session.get(uri)
        print(r.text)
        r_json = r.json()
        r_json_data = r_json['data']
        if len(r_json_data) == 0:
            return False
        return True

    def check_region(self, region: str) -> bool:
        """
        A wrapper function for is_valid_region() that conducts an
        exit if the region is non-existant.

        Returns:
            bool: True: Region is valid
        """  # noqa
        if not self.is_valid_region(region):
            raise PyForks.exceptions.InvalidRegion(
                msg=f"[!] {region} is not a valid Trailforks Region."
            )
        return True

    def __enrich_ridecounts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes in a Pandas Dataframe with messy data from Trailforks
        and cleans it up, adds values, and simply just normalizes it

        Args:
            df (pd.DataFrame): Raw Trailforks Data

        Returns:
            pd.DataFrame: Clean and Encriched Trailforks Data
        """  # noqa
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["weekday_num"] = df["date"].dt.weekday
        df["weekday"] = df["date"].dt.day_name()
        df["month_name"] = df["month"].apply(lambda x: calendar.month_abbr[x])

        return df

    
    @authentication
    def get_region_ridecounts(self, region: str) -> pd.DataFrame:
        """
        Creates a dataframe that contains that year-month-day and the
        number of rides associated with that day.

        Args:
            region (str): URI name of the region

        Returns:
            pd.DataFrame: pd.Dataframe(columns=["date","rides"])
        """
         # noqa
        rows_per_pull = 500
        page_number = 0
        enumerated_results = 0
        fields = self.uri_encode("created")
        region_id = self.get_region_id_by_alias(region)
        region_info = self.get_region_info(region)
        total_ridelogs = int(region_info["ridden"])
        region_filter = self.uri_encode(f"::{region_id}")
        dfs = []


        while enumerated_results < total_ridelogs:
            try:
                url = f"https://www.trailforks.com/api/1/ridelogs?fields={fields}&filter=rid{region_filter}&rows={rows_per_pull}&page={page_number}&order=desc&sort=created&app_id={self.app_id}&app_secret={self.app_secret}"
                r = self.trailforks_session.get(url)
                url_json = r.json()
                url_json_data = url_json["data"]
                dfs.append(pd.json_normalize(url_json_data))
                page_number += 1
                enumerated_results += rows_per_pull
            except Exception as e:
                logging.error(f"get_region_ridecounts_api();Error:{str(e)}")
                break
        
        df = pd.concat(dfs, ignore_index=True)
        df["date"] = pd.to_datetime(df['created'],unit="s").dt.strftime("%Y-%m-%d")
        t_df = df.groupby(['date'], sort=False)['date'].count().sort_index(ascending=False).reset_index(name="rides")
        return self.__enrich_ridecounts(t_df)

    def _clean_region_trails(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the region traillog data by converting distance data into
        a useable metric (miles).

        Args:
            df (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """  # noqa

        df["total_miles"] = None
        df["descent_miles"] = None
        df["ascent_miles"] = None
        df["flat_miles"] = None
        for index, row in df.iterrows():
            df.loc[index, "total_miles"] = self.feet_to_miles(str(row["distance"]))
            df.loc[index, "descent_miles"] = self.feet_to_miles(str(row["dst_descent"]))
            df.loc[index, "ascent_miles"] = self.feet_to_miles(str(row["dst_climb"]))
            df.loc[index, "flat_miles"] = self.feet_to_miles(str(row["dst_flat"]))
        df["total_miles"] = df["total_miles"].astype(float)
        df["descent_miles"] = df["descent_miles"].astype(float)
        df["ascent_miles"] = df["ascent_miles"].astype(float)
        df["flat_miles"] = df["flat_miles"].astype(float)

        return df

    def _clean_raw_csv_data(self, raw_data: str) -> str:
        """
        Trailforks CSV data is pretty bad in terms of quality. We
        need to clean things up quite a bit to get it into a dataframe

        Args:
            raw_data (str): raw CSV data

        Returns:
            str: cleaned csv data
        """  # noqa
        fix_csv_data = re.sub(r"\nhttps", '","https', raw_data)
        csv_data_list = []
        for line in fix_csv_data.split("\n"):
            line = line.strip()  # remove un-needed chars

            if "title" not in line:
                line = line[:-1]

            csv_data_list.append(line)

        return "\n".join(csv_data_list)

    @authentication
    def get_all_region_trails(self, region: str) -> pd.DataFrame:
        """
        Each region has a CSV export capability to export all trails within the region.
        This function automates that export for the end user and saves a csv to local
        disk. Ideally, this should be handled by the Trailforks API but,
        they've not provisioning access at this point (https://www.trailforks.com/about/api/)

        Args:
            region (str): region name as is shows on a URI
            region_id (str): this is the integer (string representation) of the region
            output_path (str, optional): output directory for the CSV. Defaults to ".".

        Returns:
            DataFrame: Pandas DataFrame
        """  # noqa

        fields = self.uri_encode("created,title,difficulty,physical_rating,total_jumps,total_poi,alias,faved,stats")
        region_id = self.get_region_id_by_alias(region)
        region_filter = self.uri_encode(f"rid::{region_id}")
        rows = 100
        url = f"https://www.trailforks.com/api/1/trails?scope=full&fields={fields}&filter={region_filter}&rows={rows}&app_id={self.app_id}&app_secret={self.app_secret}"
        r = self.trailforks_session.get(url)
        url_json = r.json()
        url_json_data = url_json["data"]
        df = pd.json_normalize(url_json_data)
        return df

    @authentication
    def get_all_region_ridelogs(self, region: str, pages=1) -> pd.DataFrame:
        """
        Downloads all of the trail ridelogs since the begining of the
        trails existance and stores the results in CSV format on the
        local disk. Ideally, this should be handled by the Trailforks API but,
        they've not provisioning access at this point (https://www.trailforks.com/about/api)

        Args:
            region (str): region name as is shows on a URI
            pages(int): The number of pages (HTML) to enumerate 1page == ~100 rides

        Returns:
            bool: Pandas DataFrame
        """  # noqa

        def get_date_string(row) -> int:
            epoch = float(row["created"])
            date = datetime.fromtimestamp(epoch).strftime("%m/%d/%Y")
            return date


        rows_per_pull = 100
        page_number = 0
        fields = self.uri_encode("note,created,location_name,location_id,year,device_name,username")
        region_id = self.get_region_id_by_alias(region)
        region_filter = self.uri_encode(f"::{region_id}")
        dfs = []

        logging.debug(f"get_all_region_ridelogs():region_id:{region_id}")

        for i in range(0,pages):
            url = f"https://www.trailforks.com/api/1/ridelogs?fields={fields}&filter=rid{region_filter}&rows={rows_per_pull}&page={page_number}&order=desc&sort=created&app_id={self.app_id}&app_secret={self.app_secret}"
            logging.debug(f"get_all_region_ridelogs();URL:{url}")
            r = self.trailforks_session.get(url)
            url_json = r.json()
            url_json_data = url_json["data"]
            dfs.append(pd.json_normalize(url_json_data))
            page_number += 1
        
        final_df = pd.concat(dfs, ignore_index=True)
        final_df["date"] = final_df.apply(get_date_string, axis=1)
        return final_df

    def get_region_id_by_alias(self, region_alias: str) -> int:
        """
        Given a region alias (the URI name of the region), obtain the region
        id (int) and return it

        Args:
            region_alias (str): URI name of the region

        Returns:
            int: Trailforks Region ID
        """
        df = pd.read_parquet(self.region_data_file, engine="pyarrow")
        region_id = df.loc[df["alias"] == region_alias, 'rid'].item()
        return region_id
    
    @authentication
    def get_region_info(self, region: str) -> dict:
        """
        Pulls region specific metrics from the region page. This whole function
        is an abomination (I know) but, until Trailforks publishes an API I do
        not see another way around this.

        Args:
            region (str): region name as is shows on a URI

        Returns:
            dict: {total_ridelogs, unique_riders, trails_ridden, avg_trails_per_ride}
        """  # noqa
        region_id = self.get_region_id_by_alias(region)
        url = f"https://www.trailforks.com/api/1/region?id={region_id}&scope=detailed&app_id={self.app_id}&app_secret={self.app_secret}"
        r = self.trailforks_session.get(url)
        r_json = r.json()
        r_json_data = r_json["data"]

        region_info = {
            "region_title": r_json_data["title"],
            "total_ridelogs": r_json_data["total_ridelogs"],
            "total_trails": r_json_data["total_trails"],
            "total_distance": self.meters_to_miles(r_json_data["total_distance"]),
            "total_descent": self.meters_to_miles(r_json_data["total_descent_distance"]),
            "highest_trailhead": self.meters_to_miles(r_json_data["highest_trailhead"]),
            "reports": r_json_data["total_reports"],
            "photos": r_json_data["total_photos"],
            "ridden": r_json_data["ridden"],
            "country": r_json_data["country_title"],
            "state_province": r_json_data["prov_title"],
            "city": r_json_data["city_title"],
            "links": r_json_data["links"],
            "favorites": r_json_data["faved"],
            "rating": r_json_data["rating"],
            "region_created": r_json_data["created"]
        }
        return region_info


    def _check_requires_region_admin(self, error_message: str) -> bool:
        """
        If we get an error on an authenticated function, it might be because
        the user in question is not a admin for the local trail/region and
        are just a standard user. This function determines this by looking at
        known error codes.

        Args:
            error_message (str): RAW Html error page

        Returns:
            bool: True:action requires admin;False:action doesn't need admin
        """  # noqa
        error_messages = ["Only trusted users can export"]
        return any([x in error_message for x in error_messages])

    def _thread_get_regions(self, page_number: int) -> pd.DataFrame: # noqa
        """
        Used to parallelize (yes yes, GIL I know...) the regions lookup

        Args:
            page_number (int): URI Page Number to query

        Returns:
            pd.DataFrame: Dataframe of the HTML table enumerated
        """
        uri = f"https://www.trailforks.com/regions/list/?activitytype=1&page={page_number}"
        r = self.trailforks_session.get(uri)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find('table', {"class": "table1"})
        uri_list = [tag.find("a")["href"] for tag in table.select("td:has(a)")]
        df = pd.read_html(table.prettify(), index_col=None, header=0)
        df = df[0]
        df["region_link"] = uri_list
        return df

    @authentication
    def get_all_trailforks_regions(self) -> pd.DataFrame: # noqa
        """
        BETA FUNCTION - retrieves all of the regions Trailforks knows about

        Returns:
            pd.DataFrame: DataFrame of all region data
        """
        number_of_regions = 32789
        enumerated_results = 0
        page_number = 0
        results_per_page = 50
        dfs = []

        pbar = tqdm(total=number_of_regions)
        while enumerated_results <= number_of_regions:
            url = f"https://www.trailforks.com/api/1/regions?scope=basic&app_id={self.app_id}&app_secret={self.app_secret}&rows={results_per_page}&page={page_number}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100102 Firefox/102.0"
            }
            t = self.trailforks_session.get(url, headers=headers, allow_redirects=True)
            t_json = t.json()
            dfs.append(pd.json_normalize(t_json["data"]))
            page_number += 1
            enumerated_results += results_per_page
            pbar.update(results_per_page)
        pbar.close()
        final_df = pd.concat(dfs)

        return final_df

