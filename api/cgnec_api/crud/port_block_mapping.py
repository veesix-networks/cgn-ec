from datetime import datetime
from sqlmodel import select, Session

from cgnec_api.crud.base import CRUDBase
from cgnec_api.models import NATPortBlockMapping


class CRUDPortBlockMapping(CRUDBase[NATPortBlockMapping, None, None]):
    async def get_by_x_ip_and_port(
        self,
        db: Session,
        timestamp_lt: datetime,
        timestamp_gt: datetime,
        x_ip: str = None,
        start_port: int = None,
        end_port: int = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[NATPortBlockMapping]:
        filters = [
            NATPortBlockMapping.timestamp <= timestamp_lt,
            NATPortBlockMapping.timestamp >= timestamp_gt,
        ]

        if x_ip is not None:
            filters.append(NATPortBlockMapping.x_ip == x_ip)

        if start_port is not None:
            filters.append(NATPortBlockMapping.start_port == start_port)

        if end_port is not None:
            filters.append(NATPortBlockMapping.end_port == end_port)

        query = select(NATPortBlockMapping).where(*filters).limit(limit).offset(skip)
        results = await db.exec(query)

        return results.all()


port_block_mapping = CRUDPortBlockMapping(NATPortBlockMapping)
