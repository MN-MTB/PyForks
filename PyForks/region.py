import pandas as pd
import requests
import re
import io
import calendar
from bs4 import BeautifulSoup
from tqdm import tqdm
from PyForks.trailforks import Trailforks, authentication


class Region(Trailforks):
    def is_valid_region(self, region: str) -> bool:
        """
        Check to make sure a region name is a real region by
        making sure the page title is not Error

        Returns:
            bool: True:is an existing region;False:region does not exist.
        """
        uri = f"https://www.trailforks.com/region/{region}"
        r = requests.get(uri)
        non_existent = "<title>Error</title>"
        if non_existent in r.text:
            return False
        return True

    def check_region(self, region: str) -> bool:
        """
        A wrapper function for is_valid_region() that conducts an
        exit if the region is non-existant.

        Returns:
            bool: True: Region is valid
        """
        if not self.is_valid_region(region):
            print(f"[!] {region} is not a valid Trailforks Region.")
            exit(1)
        return True

    def __enrich_ridecounts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes in a Pandas Dataframe with messy data from Trailforks
        and cleans it up, adds values, and simply just normalizes it

        Args:
            df (pd.DataFrame): Raw Trailforks Data

        Returns:
            pd.DataFrame: Clean and Encriched Trailforks Data
        """
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["weekday_num"] = df["date"].dt.weekday
        df["weekday"] = df["date"].dt.day_name()
        df["month_name"] = df["month"].apply(lambda x: calendar.month_abbr[x])

        return df

    @authentication
    def download_region_ridecounts(self, region: str) -> bool:
        """
        Downloads a regions total ridecounts is CSV format. Ideally, this should
        be handled by the Trailforks API but, they've not provisioning access
        at this point (https://www.trailforks.com/about/api/)

        Args:
            region (str): Trailforks region name per URI
            output_path (str, optional): Where to store CSV Defaults to ".".

        Returns:
            bool: true:CSV written to disk;False:failed to write CSV
        """
        self.check_region(region)
        uri = f"https://www.trailforks.com/region/{region}/ridelogcountscsv/"
        r = self.trailforks_session.get(uri, allow_redirects=True)
        raw_csv_data = r.text

        if "date,rides" in raw_csv_data:
            raw_df = pd.read_csv(io.StringIO(raw_csv_data))
            raw_df["region"] = region
            return self.__enrich_ridecounts(raw_df)

        else:
            if self._check_requires_region_admin(r.text):
                print(
                    f"[!] Error: You need to be an Admin for {region} to download Trail Ridecounts"
                )
            return pd.DataFrame

    def __clean_region_trails(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the region traillog data by converting distance data into
        a useable metric (miles).

        Args:
            df (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """

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

    def __clean_raw_csv_data(self, raw_data: str) -> str:
        """
        Trailforks CSV data is pretty bad in terms of quality. We
        need to clean things up quite a bit to get it into a dataframe

        Args:
            raw_data (str): raw CSV data

        Returns:
            str: cleaned csv data
        """
        fix_csv_data = re.sub(r"\nhttps", '","https', raw_data)
        csv_data_list = []
        for line in fix_csv_data.split("\n"):
            line = line.strip()  # remove un-needed chars

            if "title" not in line:
                line = line[:-1]

            csv_data_list.append(line)

        return "\n".join(csv_data_list)

    @authentication
    def download_all_region_trails(self, region: str, region_id: str) -> pd.DataFrame:
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
        """
        success = False
        self.check_region(region)
        uri = f"https://www.trailforks.com/tools/trailspreadsheet_csv/?cols=title,difficulty,region_title,distance,dst_climb,dst_descent,dst_flat&rid={region_id}"
        r = self.trailforks_session.get(uri, allow_redirects=True)
        raw_csv_data = r.text
        clean_csv_data = self.__clean_raw_csv_data(raw_csv_data)

        if "title,difficulty" in clean_csv_data:
            df = pd.read_csv(io.StringIO(clean_csv_data))
            return self.__clean_region_trails(df)

        else:
            if self._check_requires_region_admin(r.text):
                print(
                    f"[!] Error: You need to be an Admin for {region} to download Trail Data"
                )
            return pd.DataFrame()

    def __clean_ridelogs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Region ridelogs are messy AF! We need to normalize the distances and climb
        data for it to be useful. We will also re-name the dist and climb columns
        to denote their metric type (e.g., miles, feet, etc.)

        Args:
            df (pd.DataFrame): raw Data from Trailforks

        Returns:
            pd.DataFrame: Normalized Trailforks data
        """
        date_rex = re.compile(r"^\d{2,4}-\d{1,2}-\d{1,2}\s")
        try:
            df = df.rename(
                columns={
                    "dist": "dist_miles",
                    "climb": "climb_miles",
                    "created": "date",
                }
            )
            for index, row in df.iterrows():
                df.loc[index, "dist_miles"] = self.distance_string_to_miles_float(
                    str(row["dist_miles"])
                )
                df.loc[index, "climb_miles"] = self.distance_string_to_miles_float(
                    str(row["climb_miles"])
                )
                df.loc[index, "date"] = date_rex.findall(row["date"])[0]

            df["dist_miles"] = df["dist_miles"].astype(float)  # miles as float
            df["climb_miles"] = df["climb_miles"].astype(float)  # miles as float
            df["date"] = pd.to_datetime(df["date"])  # cast to datetime
            df["year"] = df["date"].dt.year  # get the year (int)
            df["month"] = df["date"].dt.month  # get the month (int)
            df["day"] = df["date"].dt.day  # get the day (int)
            df["weekday_num"] = df["date"].dt.weekday  # get the weekday (int)
            df["weekday"] = df["date"].dt.day_name()  # get the weekday (str)
            df["month_name"] = df["month"].apply(lambda x: calendar.month_abbr[x])
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]  # Drop unnamed columns
            df.fillna("unknown", inplace=True)

            return df
        except Exception as e:
            print(f"[!!] ERROR {e}")
            return pd.DataFrame

    @authentication
    def download_all_region_ridelogs(self, region: str) -> pd.DataFrame:
        """
        Downloads all of the trail ridelogs since the begining of the
        trails existance and stores the results in CSV format on the
        local disk. Ideally, this should be handled by the Trailforks API but,
        they've not provisioning access at this point (https://www.trailforks.com/about/api)

        Args:
            region (str): region name as is shows on a URI
            output_path (str, optional): Path to store csv. Defaults to ".".

        Returns:
            bool: Pandas DataFrame
        """
        self.check_region(region)
        region_info = self._get_region_info(region)
        total_pages = round(region_info["total_ridelogs"] / 90)
        dataframes_list = []

        pbar = tqdm(total=total_pages, desc=f"Enumerating {region} Rider Pages")
        for i in range(1, total_pages + 1):
            try:
                domain = f"https://www.trailforks.com/region/{region}/ridelogs/?viewMode=table&page={i}"
                tmp_df = pd.read_html(domain, index_col=None, header=0)
                # Sometimes we have more than 1 table on the page.
                if len(tmp_df) >= 2:
                    for potential_df in tmp_df:
                        if "city" not in potential_df.columns:
                            good_df = potential_df
                            dataframes_list.append(good_df)
                else:
                    good_df = tmp_df[0]
                    dataframes_list.append(good_df)

                pbar.update(1)
            except Exception as e:
                print(e)
                pbar.update(1)
                break
        pbar.close()

        try:
            df = pd.concat(dataframes_list, ignore_index=True)
            df["region"] = region
            return self.__clean_ridelogs(df)
        except Exception as e:
            print(f"[!] Error: {e}")
            return pd.DataFrame

    def _get_region_info(self, region: str) -> dict:
        """
        Pulls region specific metrics from the region page

        Args:
            region (str): region name as is shows on a URI

        Returns:
            dict: {total_ridelogs, unique_riders, trails_ridden, avg_trails_per_ride}
        """
        region_uri = f"https://www.trailforks.com/region/{region}/ridelogstats/"
        page = requests.get(region_uri)
        soup = BeautifulSoup(page.text, "html.parser")
        data = soup.find_all("div", class_="col-2 center")
        data = str(data[0])
        soup_1 = BeautifulSoup(data, "html.parser")
        list_items = soup_1.find_all("li")

        region_info = {
            "total_ridelogs": None,
            "unique_riders": None,
            "trails_ridden": None,
            "average_trails_per_ride": None,
        }
        region_vars = [
            "total_ridelogs",
            "unique_riders",
            "trails_ridden",
            "average_trails_per_ride",
        ]

        for i, item in enumerate(list_items):
            region_info[region_vars[i]] = int(
                re.search(r">([0-9].*)<", str(item)).groups()[0].replace(",", "")
            )

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
        """
        error_messages = ["Only trusted users can export"]
        return any([x in error_message for x in error_messages])
