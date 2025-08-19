import os
import httpx
import logging

from datetime import datetime, time
from .models import PaginatedTransactions
from .httpx_exception_handler import handle_httpx_errors


BASE_URL = os.getenv("BASE_CLIENT_URL")
HEADERS = {"content-type": "application/json"}

logger = logging.getLogger("uvicorn.error")


def stream_transactions(date, merchant):
    """
    Fetch transactions page-by-page and yield each transaction.
    Stop immediately if an httpx or remote service error occurs.
    """
    logger.info("Streaming transactions from remote server")

    # start and end of day
    settlement_s_dt = datetime.combine(date, time(0, 0, 0))
    settlement_e_dt = datetime.combine(date, time(23, 59, 59))

    current_page = 1
    url = "/transactions/"

    while True:
        params = {
            "merchant": merchant,
            "created_at__gte": settlement_s_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "created_at__lte": settlement_e_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "page": current_page,
        }

        try:
            with httpx.Client(base_url=BASE_URL, headers=HEADERS) as client:
                response = client.get(url, params=params)
                logger.info(
                    "Request Count: %i, Response Status Code: %i",
                    current_page,
                    response.status_code,
                )

                # classify upstream/downstream
                handle_httpx_errors(response=response)
                response.raise_for_status()

                paginated_transactions = PaginatedTransactions.model_validate(
                    response.json()
                )

                # Yield transactions from this page
                for txn in paginated_transactions.results:
                    yield txn

                current_page += 1

                if not paginated_transactions.next:
                    break

        except httpx.HTTPError as exc:
            logger.error("Error during streaming transactions", exc_info=True)
            handle_httpx_errors(exc=exc)
