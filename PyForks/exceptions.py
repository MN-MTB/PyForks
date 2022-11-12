class InvalidRegion(Exception):
    def __init__(self, msg="Not a valid Trailforks Region", *args, **kwargs):
        """
        Invalid Trailforks Region Exception Handler

        Args:
            msg (str, optional): Message that's presented to the user. Defaults to 'Not a valid Trailforks Region'.
        """  # noqa
        super().__init__(msg, *args, **kwargs)


class InvalidUser(Exception):
    def __init__(self, msg="Not a valid Trailforks User", *args, **kwargs):
        """
        Invalid Trailforks User Exception Handler

        Args:
            msg (str, optional): Message that's presented to the user. Defaults to 'Not a valid Trailforks User'.
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


class BadCookieError(Exception):
    def __init__(
        self,
        msg="Bad cookie file. Please delete the .cookie file and try again",
        *args,
        **kwargs
    ):
        """
        User does not have necessary permissions exception handler

        Args:
            msg (str, optional): Message that's presented to the user. Defaults to '"Bad cookie file. Please delete the .cookie file and try again'.
        """  # noqa
        super().__init__(msg, *args, **kwargs)
