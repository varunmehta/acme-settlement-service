# Put all exceptions here for now.


class HttpClientError(Exception):
    """
    Raised for errors caused by the local HTTP client setup or network issues.
    """

    def __init__(self, detail: str):
        self.detail = detail


class RemoteServiceError(Exception):
    """
    Raised for errors returned from the remote service.
    """

    def __init__(self, detail: str):
        self.detail = detail
