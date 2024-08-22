class InvalidRegion(Exception):
    def __init__(self, msg="Not a valid Trailforks Region", *args, **kwargs):
        """
        Invalid Trailforks Region Exception Handler

        Args:
            msg (str, optional): Message that's presented to the user. Defaults to 'Not a valid Trailforks Region'.
        """  # noqa
        super().__init__(msg, *args, **kwargs)

class InvalidPermissions(Exception):
    def __init__(self, msg="Invalid Permissions", *args, **kwargs):
        """
        User does not have necessary permissions exception handler

        Args:
            msg (str, optional): Message that's presented to the user. Defaults to 'Invalid Permissions'.
        """  # noqa
        super().__init__(msg, *args, **kwargs)


class RegionLockedAPI(Exception):
    def __init__(self, msg="Invalid Permissions", *args, **kwargs):
        """
        User has a regional locked API token for their app_id/app_secret

        Args:
            msg (str, optional): _description_. Defaults to "Invalid Permissions".
        """
        super().__init__(msg, *args, **kwargs)


class TrailforksAPIException(Exception):
    def __init__(self, msg="Invalid Permissions", *args, **kwargs):
        """
        Generic Trailforks ARest API exception Handler

        Args:
            msg (str, optional): _description_. Defaults to "Invalid Permissions".
        """
        super().__init__(msg, *args, **kwargs)
