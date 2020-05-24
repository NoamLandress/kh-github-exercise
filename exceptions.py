class AuthenticationDetailsNotGiven(Exception):
    """
    Creates a Unique Exception for when authentication details were not supplied by the user
    """

    def __init__(self):
        super().__init__("Authentication details were not entered for user")


class HttpResponseError(Exception):
    """
    Creates a Unique Exception for when the HTTP response is not valid (200 OK)
    """

    def __init__(self, status_code):
        super().__init__(f"Unable to Make API call, error code:{status_code}")
