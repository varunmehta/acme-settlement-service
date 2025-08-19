import httpx
import logging

from typing import Optional

from ..exceptions import HttpClientError, RemoteServiceError


logger = logging.getLogger("uvicorn.error")


def handle_httpx_errors(
    response: Optional[httpx.Response] = None, exc: Optional[Exception] = None
):
    # Handle network and client errors
    if exc:
        if isinstance(
            exc,
            (
                httpx.ConnectError,
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
                httpx.PoolTimeout,
                httpx.InvalidURL,
                httpx.UnsupportedProtocol,
                httpx.NetworkError,
            ),
        ):
            logger.error("Error occurred making a request: ", exc, stack_info=True)
            raise HttpClientError(f"HTTP client error: {exc}") from exc

        logger.error("Error occurred making a request: ", exc, stack_info=True)
        # Generic unexpected httpx exception
        raise HttpClientError(f"Unexpected HTTP client error: {exc}") from exc

    # Handle server-side errors
    if response is not None:
        logger.info("Response received with status_code: %s", response.status_code)

        if 500 <= response.status_code < 600:
            logger.error("Error occurred at the remote service %s", response.text)
            raise RemoteServiceError(
                "Error occurred at the source service, please try again."
            )
        elif 400 <= response.status_code < 500:
            # Some 400s thrown by remote server are also to be propagated back
            logger.error(
                "Error with status_code %s at the remote service %s",
                response.status_code,
                response.text,
            )
            raise HttpClientError(f"Bad request to remote service: {response.text}")
