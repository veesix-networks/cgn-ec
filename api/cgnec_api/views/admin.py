from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from cgnec_api.config import settings
from cgnec_api.dependencies import DatabaseDep
from cgnec_api import crud
from cgnec_api.models import NATAddressMapping

router = APIRouter()


@router.get("/hypertable/{hyper_table}/chunks")
async def get_hyper_table_chunks(db: DatabaseDep, hyper_table: str):
    hypertable_exist = await crud.admin.check_hypertable_exist(db, hyper_table)
    if not hypertable_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hypertable named '{hyper_table}'.",
        )

    chunks = await crud.admin.get_hypertable_chunks(db, hyper_table)
    return chunks
