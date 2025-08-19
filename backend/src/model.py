from enum import Enum
from decimal import Decimal
from datetime import date

from typing import List, Optional

from pydantic import BaseModel, AnyUrl, UUID4

# --------
# Ideally this should split into it's own folder
# and can be used with routes in fastapi,
# but since this is a simple API for now,
# keeping all models at root level.


# Query Parameter Model
# ---------------------
class SettlementParams(BaseModel):
    model_config = {"extra": "forbid"}
    merchant: UUID4
    date: date


#  Response Models
# ----------------
class Settlement(BaseModel):
    date: date
    merchant: UUID4
    sale: Decimal
    refund: Decimal
    total: Decimal


# -- models, for serving the UI
# TODO: make REST endpoints available to consume data


class PaymentTypeEnum(Enum):
    PURCHASE = "PURCHASE"
    REFUND = "REFUND"
    # manually added, doc says `PURCHASE`, response was `SALE`
    SALE = "SALE"


class Transaction(BaseModel):
    id: UUID4
    amount: Decimal
    type: PaymentTypeEnum
    customer: UUID4
    merchant: UUID4
    order: UUID4


# - Provide a deep-dive into settlements for self reconciliation.
class SettlementDetails(Settlement):
    transactions: Optional[List[Transaction]] | None


class Merchant(BaseModel):
    id: UUID4
    name: str


class PaginatedMerchant(BaseModel):
    count: int
    next: Optional[AnyUrl] | None
    previous: Optional[AnyUrl] | None
    results: Optional[List[Merchant]] | None
