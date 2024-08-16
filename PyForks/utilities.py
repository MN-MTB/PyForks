import pandas as pd
import logging
from datetime import datetime
import PyForks.exceptions
import calendar
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
        json_response = self.make_trailforks_request(uri)
        if len(json_response) == 0:
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
            pd.DataFrame: adds new datetime columns (columns=[year,month,day,weekday_num,weekday,month_name])
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
    def get_region_ridecounts_by_rider(self, region: str) -> pd.DataFrame:
        """
        Creates a dataframe that contains a username and the
        number of rides associated with that user.

        Args:
            region (str): URI name of the region

        Returns:
            pd.DataFrame: pd.DataFrame(columns=["username","rides"])
        """ # noqa
        self.check_region(region)
        rows_per_pull = 8000
        page_number = 0
        enumerated_results = 0
        fields = self.uri_encode("created,username")
        region_id = self.get_region_id_by_alias(region)
        region_info = self.get_region_info(region)
        total_ridelogs = int(region_info["ridden"])
        region_filter = self.uri_encode(f"::{region_id}")
        dfs = []

        threads = []
        with ThreadPoolExecutor() as executor:

            while enumerated_results < total_ridelogs:
                uri = f"https://www.trailforks.com/api/1/ridelogs?fields={fields}&filter=rid{region_filter}&rows={rows_per_pull}&page={page_number}&order=desc&sort=created&app_id={self.app_id}&app_secret={self.app_secret}"
                threads.append(executor.submit(self.make_trailforks_request, uri))
                page_number += 1
                enumerated_results += rows_per_pull
                
            for job in as_completed(threads):
                json_response = job.result()
                dfs.append(pd.json_normalize(json_response))

        df = pd.concat(dfs, ignore_index=True)
        t_df = df.groupby(['username'], sort=True).count().sort_values(by='created', ascending=False).reset_index()
        t_df.rename(columns={'created':'rides'}, inplace=True)
        return t_df
    

    @authentication
    def get_region_ridecounts(self, region: str) -> pd.DataFrame:
        """
        Creates a dataframe that contains that year-month-day and the
        number of rides associated with that day.

        Args:
            region (str): URI name of the region

        Returns:
            pd.DataFrame: pd.DataFrame(columns=["date","rides"])
        """ # noqa
        self.check_region(region)
        rows_per_pull = 10000
        page_number = 0
        enumerated_results = 0
        fields = self.uri_encode("created")
        region_id = self.get_region_id_by_alias(region)
        region_info = self.get_region_info(region)
        total_ridelogs = int(region_info["ridden"])
        region_filter = self.uri_encode(f"::{region_id}")
        dfs = []

        threads = []
        with ThreadPoolExecutor() as executor:

            while enumerated_results < total_ridelogs:
                uri = f"https://www.trailforks.com/api/1/ridelogs?fields={fields}&filter=rid{region_filter}&rows={rows_per_pull}&page={page_number}&order=desc&sort=created&app_id={self.app_id}&app_secret={self.app_secret}"
                threads.append(executor.submit(self.make_trailforks_request, uri))
                page_number += 1
                enumerated_results += rows_per_pull
                
            for job in as_completed(threads):
                json_response = job.result()
                dfs.append(pd.json_normalize(json_response))

        df = pd.concat(dfs, ignore_index=True)
        df["date"] = pd.to_datetime(df['created'],unit="s").dt.strftime("%Y-%m-%d")
        t_df = df.groupby(['date'], sort=False)['date'].count().sort_index(ascending=False).reset_index(name="rides")
        return self.__enrich_ridecounts(t_df)

    @authentication
    def get_all_region_trails(self, region: str) -> pd.DataFrame:
        """
        Queries the Trailforks Trails API to obtain trail information for
        a given region

        Args:
            region (str): region uri name (alias)

        Returns:
            pd.DataFrame: Pandas DataFrame(columns=[created,title,difficulty,physical_rating,total_jumps,total_poi,alias,faved,stats])
        """
         # noqa
        self.check_region(region)
        fields = self.uri_encode("created,title,difficulty,physical_rating,total_jumps,total_poi,alias,faved,stats")
        region_id = self.get_region_id_by_alias(region)
        region_filter = self.uri_encode(f"rid::{region_id}")
        rows = 100
        uri = f"https://www.trailforks.com/api/1/trails?scope=full&fields={fields}&filter={region_filter}&rows={rows}&app_id={self.app_id}&app_secret={self.app_secret}"
        json_response = self.make_trailforks_request(uri)
        df = pd.json_normalize(json_response)
        return df

    @authentication
    def get_all_region_ridelogs(self, region: str, pages=1) -> pd.DataFrame:
        """
        Downloads all of the trail ridelogs since the beginning of the
        trails existence and stores the results in CSV format on the
        local disk. Ideally, this should be handled by the Trailforks API but,
        they've not provisioning access at this point (https://www.trailforks.com/about/api)

        Args:
            region (str): region name as is shows on a URI
            pages(int): The number of pages (HTML) to enumerate 1page == ~100 rides

        Returns:
            bool: Pandas DataFrame(columns=[note,created,location_name,location_id,year,device_name,username])
        """  # noqa
        self.check_region(region)
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

        for i in range(0,pages):
            uri = f"https://www.trailforks.com/api/1/ridelogs?fields={fields}&filter=rid{region_filter}&rows={rows_per_pull}&page={page_number}&order=desc&sort=created&app_id={self.app_id}&app_secret={self.app_secret}"
            json_response = self.make_trailforks_request(uri)
            dfs.append(pd.json_normalize(json_response))
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
            dict: {
                region_title:       string,
                total_ridelogs:     int,
                total_trails:       int,
                total_distance:     float,
                total_descent:      float,
                highest_trailhead:  float,
                reports:            int,
                photos:             int,
                ridden:             int,
                country:            string,
                state_province:     string,
                city:               string,
                links:              list,
                favorites:          int,
                rating:             int,
                region_created      int
            }
        """  # noqa
        self.check_region(region)
        region_id = self.get_region_id_by_alias(region)
        uri = f"https://www.trailforks.com/api/1/region?id={region_id}&scope=detailed&app_id={self.app_id}&app_secret={self.app_secret}"
        json_response = self.make_trailforks_request(uri)

        region_info = {
            "region_title": json_response["title"],
            "total_ridelogs": json_response["total_ridelogs"],
            "total_trails": json_response["total_trails"],
            "total_distance": self.meters_to_miles(json_response["total_distance"]),
            "total_descent": self.meters_to_miles(json_response["total_descent_distance"]),
            "highest_trailhead": self.meters_to_miles(json_response["highest_trailhead"]),
            "reports": json_response["total_reports"],
            "photos": json_response["total_photos"],
            "ridden": json_response["ridden"],
            "country": json_response["country_title"],
            "state_province": json_response["prov_title"],
            "city": json_response["city_title"],
            "links": json_response["links"],
            "favorites": json_response["faved"],
            "rating": json_response["rating"],
            "region_created": json_response["created"]
        }
        return region_info

    @authentication
    def get_all_trailforks_regions(self, number_of_regions=40_000) -> pd.DataFrame: 
        """
        Retrieve all known regions listed on Trailforks or a subset of regions
        subject to the number_of_regions parameter

        Args:
            number_of_regions (int, optional): Number of regions to pull. Defaults to 40_000 and the minimum is 500.

        Returns:
            pd.DataFrame: DataFrame(columns=['rid', 'title', 'alias'])
        """
         # noqa
        enumerated_results = 0
        page_number = 0
        results_per_page = 500
        fields = self.uri_encode("rid,title,alias,country_title,prov_title,city_title")
        dfs = []

        pbar = tqdm(total=number_of_regions)
        while enumerated_results <= number_of_regions:
            uri = f"https://www.trailforks.com/api/1/regions?scope=basic&app_id={self.app_id}&fields={fields}&app_secret={self.app_secret}&rows={results_per_page}&page={page_number}"
            json_response = self.make_trailforks_request(uri)
            dfs.append(pd.json_normalize(json_response))
            page_number += 1
            enumerated_results += results_per_page
            pbar.update(results_per_page)
        pbar.close()
        final_df = pd.concat(dfs)
        final_df.astype(str).drop_duplicates(inplace=True)
        return final_df


    @authentication
    def get_region_photos(self, region: str) -> list:
        """
        Get a list of photos taken by riders for a specific region

        Args:
            region (str): Region URI Name

        Returns:
            list: List of pinkbike photo links
        """
        self.check_region(region)
        photos = []
        region_id = self.get_region_id_by_alias(region)
        region_filter = self.uri_encode(f"::{region_id}")
        uri = f"https://www.trailforks.com/api/1/photos?filter=rid{region_filter}&rows=20&order=desc&app_id={self.app_id}&app_secret={self.app_secret}"
        json_response = self.make_trailforks_request(uri)
        for obj in json_response:
            photos.append(obj.get('thumbs', {}).get("l", None))
        return photos
    
    @authentication
    def get_region_videos(self, region: str) -> dict:
        """
        Get a dict of videos taken by riders for a specific region

        Args:
            region (str): Region URI Name

        Returns:
            dict: Dict{videos: [{source, source_id, source_url}]}
        """
        self.check_region(region)
        videos = {'videos': []}
        region_id = self.get_region_id_by_alias(region)
        region_filter = self.uri_encode(f"::{region_id}")
        uri = f"https://www.trailforks.com/api/1/videos?filter=rid{region_filter}&rows=20&order=desc&app_id={self.app_id}&app_secret={self.app_secret}"
        json_response = self.make_trailforks_request(uri)
        for obj in json_response:
            source = obj.get('source', None)
            # Source is either youtube or pb
            if source == "youtube":
                id = obj.get('source_id', None)
                url = obj.get('source_url', None)
                videos['videos'].append({'source': source, 'id':id, 'url':url})
            else:
                id = obj.get('id', None)
                url = obj.get('media', {}).get('s1080', None)
                videos['videos'].append({'source': source, 'id':id, 'url':url})
        return videos