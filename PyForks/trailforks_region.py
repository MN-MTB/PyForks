import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import as_completed, ThreadPoolExecutor
from PyForks.trailforks import Trailforks, authentication

class TrailforksRegion(Trailforks):

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

    @authentication
    def download_region_ridecounts(self, region: str, output_path=".") -> bool:
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
        success = False
        self.check_region(region)
        uri = f"https://www.trailforks.com/region/{region}/ridelogcountscsv/"
        r = self.trailforks_session.get(uri, allow_redirects=True)
        raw_csv_data = r.text
        
        if "date,rides" in raw_csv_data:
            open(f"{output_path}/{region}_ridelogcounts.csv", "w").write(raw_csv_data)
            success = True
        else:
            if self._check_requires_region_admin(r.text):
                print(f"[!] Error: You need to be an Admin for {region} to download Trail Ridecounts")

        return success

    @authentication
    def download_all_region_trails(self, region: str, region_id: str, output_path=".") -> bool:
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
            bool: true:CSV written to disk;False:failed to write CSV
        """
        success = False
        self.check_region(region)
        uri = f"https://www.trailforks.com/tools/trailspreadsheet_csv/?cols=trailid,title,aka,activitytype,difficulty,status,condition,region_title,rid,difficulty_system,trailtype,usage,direction,season,unsanctioned,hidden,rating,ridden,total_checkins,total_reports,total_photos,total_videos,faved,views,global_rank,created,land_manager,closed,wet_weather,distance,time,alt_change,alt_max,alt_climb,alt_descent,grade,dst_climb,dst_descent,dst_flat,alias,inventory_exclude,trail_association,sponsors,builders,maintainers&rid={region_id}"
        r = self.trailforks_session.get(uri, allow_redirects=True)
        raw_csv_data = r.text
        clean_data = re.sub(r'[aA-zZ]\n', "\",", raw_csv_data)

        if "trailid,title" in clean_data:
            success = True
            open(f"{output_path}/{region}_trail_listing.csv", "w").write(clean_data)
        else:
            if self._check_requires_region_admin(r.text):
                print(f"[!] Error: You need to be an Admin for {region} to download Trail Data")

        return success

    @authentication
    def download_all_region_ridelogs(self, region: str, output_path=".") -> bool:
        """
        Downloads all of the trail ridelogs since the begining of the 
        trails existance and stores the results in CSV format on the 
        local disk. Ideally, this should be handled by the Trailforks API but,
        they've not provisioning access at this point (https://www.trailforks.com/about/api)

        Args:
            region (str): region name as is shows on a URI
            output_path (str, optional): Path to store csv. Defaults to ".".
            
        Returns:
            bool: true:CSV written to disk;False:failed to write CSV
        """
        self.check_region(region)
        region_info = self._get_region_info(region)
        total_pages = round(region_info["total_ridelogs"]/90)
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
                pbar.update(1)
                break
        pbar.close()

        try:
            df = pd.concat(dataframes_list, axis=0, ignore_index=True)
            df.to_csv(f"{output_path}/{region}_scraped_riders.csv")
            return True
        except:
            return False


    def _get_region_info(self, region: str) -> dict:
        """
        Pulls region specific metrics from the region page

        Args:
            region (str): region name as is shows on a URI

        Returns:
            dict: {total_ridelogs, unique_riders, trails_ridden, avg_trails_per_ride}
        """
        region_uri = f'https://www.trailforks.com/region/{region}/ridelogstats/'
        page = requests.get(region_uri)
        soup = BeautifulSoup(page.text, 'html.parser')
        data = soup.find_all("div", class_="col-2 center")
        data = str(data[0])
        soup_1 = BeautifulSoup(data, "html.parser")
        list_items = soup_1.find_all("li")

        region_info = {
            "total_ridelogs": None,
            "unique_riders": None,
            "trails_ridden": None,
            "average_trails_per_ride": None
        }
        region_vars = ["total_ridelogs", "unique_riders", "trails_ridden", "average_trails_per_ride"]

        for i, item in enumerate(list_items):
            region_info[region_vars[i]] = int(re.search(r'>([0-9].*)<', str(item)).groups()[0].replace(",",""))
        
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
