class ValidationError(Exception):
    """
    Any error that happens during the validation process of a response
    """
    pass


class ApiResponseError(Exception):
    """
    Any error that happens during the connection to the Premiumize api
    """

    def __init__(self, api_response):
        self.status = api_response.status
        self.message = str(self.status) + " - " + api_response.message
        super().__init__(self.message)


class ApiRequestError(Exception):
    """
    Any error that happens during the request phase
    """

    def __init__(self, message):
        super().__init__(message)


