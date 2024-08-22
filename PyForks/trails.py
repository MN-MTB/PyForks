from PyForks.trailforks import Trailforks
from typing import Any, Dict

class Trails(Trailforks):

    def get_map_trails(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of trails within a bounding box for displaying on a map.

        Args:
            **kwargs: Optional parameters such as:
                output (str): Output format of the trails, default is Google encoded path.
                filter (str): Filter variables in the format 'field::value;field2::value2'.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/maptrails", params=kwargs)
        return response.json()
    
    def get_trail(self, id: int, **kwargs) -> Dict[str, Any]:
        """
        Return a specific trail.

        Args:
            id (int): ID of the trail.
            **kwargs: Optional parameters such as:
                scope (str): Detail of trail object to return.
                fields (str): Limit the fields returned.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        params = {'id': id}
        params.update(kwargs)
        response = self._get(f"{self.base_uri}/trail", params=params)
        return response.json()
    
    def get_trail_status(self, since: int, **kwargs) -> Dict[str, Any]:
        """
        Return trail status & condition for trails in region.

        Args:
            since (int): Timestamp to return status after.
            **kwargs: Optional parameters such as:
                rids (str): Comma-separated list of region IDs.
                trailids (str): Comma-separated list of trail IDs.
                reportdetail (int): Show details of the most recent trail report.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        params = {'since': since}
        params.update(kwargs)
        response = self._get(f"{self.base_uri}/trail_status", params=params)
        return response.json()
    
    def get_trails(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of trails.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of trail object to return.
                fields (str): Limit the fields returned by a comma-separated list of allowed fields.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of trails to return, max 500.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/trails", params=kwargs)
        return response.json()
    
    # POST functions require a User authentication token. The Trailforks API does not have a public endpoint 
    # for this capability such that we can create a User Access Token via the REST API. We will have to build
    # this functionality into the PyForks library in the future. In searching for a login endpoint, we found 
    # https://www.trailforks.com/api/1/login to be deprecated.

    # def post_waypoint(self, activitytype: int, latitude: float, longitude: float, **kwargs) -> Dict[str, Any]:
    #     """
    #     Add a personal waypoint.

    #     Args:
    #         activitytype (int): Type of activity.
    #         latitude (float): Latitude of the waypoint.
    #         longitude (float): Longitude of the waypoint.
    #         **kwargs: Optional parameters such as:
    #             action (str): 'add' or 'edit'.
    #             title (str): Title of the waypoint.
    #             note (str): Note associated with the waypoint.
    #             color (str): HTML color code.
    #             private (int): 1 for private, 0 for public.
    #             source (str): Source of the waypoint (app or API).
    #             waypointuid (str): Unique ID for the waypoint.

    #     Returns:
    #         Dict[str, Any]: Response data from the API.
    #     """
        
    #     data = {
    #         'activitytype': activitytype,
    #         'latitude': latitude,
    #         'longitude': longitude
    #     }
    #     data.update(kwargs)
    #     response = self.trailforks_session.post(f"{self.base_uri}/waypoint", data=data)

    # def post_report(self, trailid: int, status: int, **kwargs) -> Dict[str, Any]:
    #     """
    #     Add a trail report.

    #     Args:
    #         trailid (int): ID of the trail.
    #         status (int): Status of the trail.
    #         **kwargs: Optional parameters such as:
    #             condition (int): Condition of the trail.
    #             description (str): Description of trail condition or issues.
    #             marker (str): Location of the report (lat, lon).

    #     Returns:
    #         Dict[str, Any]: Response data from the API.
    #     """
        
    #     data = {'trailid': trailid, 'status': status}
    #     data.update(kwargs)
    #     response = self.trailforks_session.post(f"{self.base_uri}/report", data=data)
    #     return response.json()
    
    def get_reports(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of reports.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of report object to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of reports to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/reports", params=kwargs)
        return response.json()