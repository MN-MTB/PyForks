from PyForks.trailforks import Trailforks
from typing import Any, Dict

class Events(Trailforks):

    def get_event(self, id: int, **kwargs) -> Dict[str, Any]:
        """
        Return a specific event.

        Args:
            id (int): ID of the event.
            **kwargs: Optional parameters such as:
                scope (str): Detail of the event object to return.
                fields (str): Limit the fields returned.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
        params = {'id': id}
        params.update(kwargs)
        response = self._get(f"{self.base_uri}/event", params=params)
        return response.json()

    def get_events(self, **kwargs) -> Dict[str, Any]:
        """
        Return a list of events.

        Args:
            **kwargs: Optional parameters such as:
                scope (str): Detail level of event object to return.
                fields (str): Limit the fields returned.
                filter (str): Filter variables in the format 'field::value;field2::value2'.
                rows (int): Number of events to return.
                page (int): Page through results.
                sort (str): Sort the results.
                order (str): Order the results.

        Returns:
            Dict[str, Any]: Response data from the API.
        """
    
        response = self._get(f"{self.base_uri}/events", params=kwargs)
        return response.json()