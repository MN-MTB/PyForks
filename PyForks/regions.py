from PyForks.trailforks import Trailforks
from typing import Any, Dict

class Regions(Trailforks):

    def get_poi(self, id: int, **kwargs) -> Dict[str, Any]:
        """
        Return a specific Point of Interest (POI).

        Args:
            id (int): ID of the POI.
            **kwargs: Optional parameters such as:
                scope (str): Detail of POI object to return.
                fields (str): Limit the fields returned.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        params = {'id': id}
        params.update(kwargs)
        response = self._get(f"{self.base_uri}/poi", params=params)
        return response.json()

    def get_region(self, id: int, **kwargs) -> Dict[str, Any]:
        """
        Return a specific region.

        Args:
            id (int): ID of the region.
            **kwargs: Optional parameters such as:
                scope (str): Detail of region object to return.
                fields (str): Limit the fields returned.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        params = {'id': id}
        params.update(kwargs)
        response = self._get(f"{self.base_uri}/region", params=params)
        return response.json()

    def get_region_status(self, since: int, **kwargs) -> Dict[str, Any]:
        """
        Return region status & condition.

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
        response = self._get(f"{self.base_uri}/region_status", params=params)
        return response.json()

    def get_regions(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of regions.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of region object to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of regions to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/regions", params=kwargs)
        return response.json()
    
    def get_ridelogs(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of ride logs for trail or region.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of ride log object to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of ride logs to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/ridelogs", params=kwargs)
        return response.json()

    # Personal Ride Plans need user authentication. We will implement this in the future since it's not a priority
    # and has to be OATH2 authenticated given the login API is deprecated.

    # def get_rideplan(self, id: int, **kwargs) -> Dict[str, Any]:
    #     """
    #     Return a specific ride plan.

    #     Args:
    #         id (int): ID of the ride plan.
    #         **kwargs: Optional parameters such as:
    #             fields (str): Limit the fields returned.

    #     Returns:
    #         Dict[str, Any]: Response data from the API.
    #     """
        
    #     params = {'id': id}
    #     params.update(kwargs)
    #     response = self._get(f"{self.base_uri}/rideplan", params=params)
    #     return response.json()

    # def get_rideplans(self, **kwargs) -> Dict[str, Any]:
    #     """
    #     Return a list of personal ride plans, must be authenticated with user token.

    #     Args:
    #         **kwargs: Optional parameters such as:
    #             scope (str): Detail level of route object to return.
    #             fields (str): Limit the fields returned.
    #             filter (str): Filter variables in the format 'field::value;field2::value2'.
    #             rows (int): Number of ride plans to return.
    #             page (int): Page through results.
    #             sort (str): Sort the results.
    #             order (str): Order the results.

    #     Returns:
    #         Dict[str, Any]: Response data from the API.
    #     """
        
    #     response = self._get(f"{self.base_uri}/rideplans", params=kwargs)
    #     return response.json()

    def get_route(self, id: int, **kwargs) -> Dict[str, Any]:
        """
        Return a specific route.

        Args:
            id (int): ID of the route.
            **kwargs: Optional parameters such as:
                scope (str): Detail of route object to return.
                fields (str): Limit the fields returned.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        params = {'id': id}
        params.update(kwargs)
        response = self._get(f"{self.base_uri}/route", params=params)
        return response.json()

    def get_routes(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of public routes.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of route object to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of routes to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/routes", params=kwargs)
        return response.json()

    def get_supporters(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of supporters for a trail, region, or route.

        Args:
            **kwargs: Optional parameters such as:
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of supporters to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/supporters", params=kwargs)
        return response.json()


    def get_videos(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of trail or region videos.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of video objects to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of videos to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/videos", params=kwargs)
        return response.json()
    
    def get_photos(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of trail or region photos.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of photo objects to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of photos to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        
        response = self._get(f"{self.base_uri}/photos", params=kwargs)
        return response.json()