import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import as_completed, ThreadPoolExecutor
from PyForks.trailforks import Trailforks

class TrailforksRegion(Trailforks):

    def is_valid_region(self) -> bool:
        uri = f"https://www.trailforks.com/region/{self.region}"
        r = requests.get(uri)
        non_existant = "<title>Error</title>"
        if non_existant in r.text:
            return False
        return True

    def download_all_region_rides(self, region_id: str, output_path=".") -> bool:
        self.check_region()
        self.check_cookie()
        uri = f"https://www.trailforks.com/tools/trailspreadsheet_csv/?cols=trailid,title,aka,activitytype,difficulty,status,condition,region_title,rid,difficulty_system,trailtype,usage,direction,season,unsanctioned,hidden,rating,ridden,total_checkins,total_reports,total_photos,total_videos,faved,views,global_rank,created,land_manager,closed,wet_weather,distance,time,alt_change,alt_max,alt_climb,alt_descent,grade,dst_climb,dst_descent,dst_flat,alias,inventory_exclude,trail_association,sponsors,builders,maintainers&rid={region_id}"
        r = requests.get(uri, cookies=self.cookie, allow_redirects=True)
        raw_csv_data = r.text
        clean_data = re.sub(r'[aA-zZ]\n', "\",", raw_csv_data)

        open(f"{output_path}/{self.region}_trail_listing.csv", "w").write(clean_data)

    def check_region(self) -> None:
        if not self.is_valid_region():
            print(f"[!] {self.region} is not a valid Trailforks Region.")
            exit(1)
