from datetime import datetime
from sqlmodel import select, Session, text

from cgnec_api.crud.base import CRUDBase


class CRUDAdmin(CRUDBase[None, None, None]):
    async def check_hypertable_exist(self, db: Session, hypertable: str) -> bool:
        query = text(
            "SELECT EXISTS (SELECT 1 FROM timescaledb_information.hypertables WHERE hypertable_name = :hypertable_name)"
        )
        result = await db.exec(query, params={"hypertable_name": hypertable})
        return result.scalar()

    async def get_hypertable_chunks(self, db: Session, hypertable: str) -> list[dict]:
        query = text(
            "SELECT * FROM timescaledb_information.chunks WHERE hypertable_name = :hypertable_name"
        )
        result = await db.exec(query, params={"hypertable_name": hypertable})
        chunks = result.fetchall()

        # If no chunks found, return empty list
        if not chunks:
            return {"hypertable": hypertable, "chunks": []}

        # Format results as a list of dictionaries
        return {
            "hypertable": hypertable,
            "chunks": [dict(row._mapping) for row in chunks],
        }


admin = CRUDAdmin(None)
