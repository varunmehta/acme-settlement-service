import logging
from typing import Annotated
from starlette import status
from fastapi import APIRouter, HTTPException, Query

from ..model import Settlement, SettlementParams
from ..services.settlement_service import calculate_settlement
from ..exceptions import HttpClientError, RemoteServiceError

logger = logging.getLogger("uvicorn.error")

router = APIRouter()


@router.get("/settlement/", response_model=Settlement)
async def settlement_endpoint(query: Annotated[SettlementParams, Query()]):
    try:
        return calculate_settlement(
            date=query.date,
            merchant=query.merchant,
        )
    except HttpClientError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong with our connection. Please try again",
        )
    except RemoteServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )
