
class InvalidRegion(Exception):
    def __init__(self, msg='Not a valid Trailforks Region', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

class InvalidUser(Exception):
    def __init__(self, msg='Not a valid Trailforks User', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

class InvalidPermissions(Exception):
    def __init__(self, msg='Invalid Permissions', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

