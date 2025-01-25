from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from cgnec_api.config import settings
from cgnec_api.dependencies import DatabaseDep
from cgnec_api import crud
from cgnec_api.models import NATPortMapping

router = APIRouter()


@router.get("/", response_model=list[NATPortMapping])
def get_port_mappings(
    db: DatabaseDep,
    x_ip: str = None,
    x_port: int = None,
    timestamp_gt: datetime = None,
    timestamp_lt: datetime = datetime.now(tz=timezone.utc),
    limit: int = 100,
    skip: int = 0,
):
    current_time_utc = datetime.now(tz=timezone.utc)

    if not timestamp_gt:
        timestamp_gt = current_time_utc - timedelta(
            hours=settings.DEFAULT_LOOKBACK_HOURS
        )

    # Validation: timestamp_lt must be less than now
    if timestamp_lt >= current_time_utc:
        raise HTTPException(
            status_code=400, detail="timestamp_lt must be less than the current time."
        )

    # Validation: timestamp_lt must be greater than timestamp_gt
    if timestamp_lt <= timestamp_gt:
        raise HTTPException(
            status_code=400, detail="timestamp_lt must be greater than timestamp_gt."
        )

    results = crud.port_mapping.get_by_x_ip_and_port(
        db, timestamp_lt, timestamp_gt, x_ip, x_port, limit, skip
    )

    return results
