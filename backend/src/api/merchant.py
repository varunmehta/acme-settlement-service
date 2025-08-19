import logging
from fastapi import APIRouter, HTTPException
from ..model import PaginatedMerchant

logger = logging.getLogger("uvicorn.error")

router = APIRouter()


# Make this end point available for UI
# to make the merchant dropdown user-friendly
@router.get("/merchants", response_model=PaginatedMerchant)
async def get_merchants():
    """
    Returns a list of merchants, for UI display purpose. Yet to be implemented.
    """
    raise HTTPException(status_code=418, detail="I'm a teapot yet to be implemented")
    return PaginatedMerchant
