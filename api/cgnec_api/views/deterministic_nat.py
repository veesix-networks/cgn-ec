from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from cgnec_api.config import settings
from cgnec_api.dependencies import DatabaseDep
from cgnec_api import crud
from cgnec_api.models import NATSessionMapping

router = APIRouter()


@router.get("/", response_model=list[NATSessionMapping])
def get_deterministic_nat_mapping(
    db: DatabaseDep,
    x_ip: str = None,
    x_port: int = None,
    timestamp_gt: datetime = None,
    timestamp_lt: datetime = datetime.now(tz=timezone.utc),
    limit: int = 100,
    skip: int = 0,
):
    return
