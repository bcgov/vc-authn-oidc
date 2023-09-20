from pymongo.errors import WriteError
from fastapi import HTTPException
from fastapi import status as http_status
import structlog

logger = structlog.getLogger(__name__)


def raise_appropriate_http_exception(err: WriteError, exists_msg: str = None):
    if err.code == 11000:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail=exists_msg,
        )
    else:
        logger.error("Unknown error", err=err)
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The server was unable to process the request",
        )


def check_and_raise_not_found_http_exception(resp, detail: str = None):
    if detail is None:
        detail = "The requested resource wasn't found"

    if resp is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
