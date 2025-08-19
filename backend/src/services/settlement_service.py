import logging
from decimal import Decimal
from tenacity import retry, wait_exponential_jitter

from ..acme_client import client, models as acme_models
from ..model import Settlement
from ..exceptions import HttpClientError, RemoteServiceError

logger = logging.getLogger("uvicorn.error")


@retry(wait=wait_exponential_jitter(initial=0.5, max=45), reraise=True)
def calculate_settlement(date, merchant):
    """
    Stream transactions from client, calculate settlement amount on the fly.

    Raise exception as soon as any fetch fails.
    """
    sale = Decimal()
    refund = Decimal()
    total = Decimal()

    try:
        for transaction in client.stream_transactions(date=date, merchant=merchant):
            if transaction.type in (
                acme_models.PaymentTypeEnum.PURCHASE,
                acme_models.PaymentTypeEnum.SALE,
            ):
                sale += transaction.amount
            elif transaction.type == acme_models.PaymentTypeEnum.REFUND:
                refund += transaction.amount

        # Once we have sale and refund, we calculate total
        total = sale - refund

    except (HttpClientError, RemoteServiceError):
        # Bubble up for FastAPI exception handler to catch
        raise

    return Settlement(
        date=date.strftime("%Y-%m-%d"),
        merchant=merchant,
        sale=sale,
        refund=refund,
        total=total,
    )
