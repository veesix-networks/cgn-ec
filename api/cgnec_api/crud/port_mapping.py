from datetime import datetime
from sqlmodel import select, Session

from cgnec_api.crud.base import CRUDBase
from cgnec_api.models import NATPortMapping


class CRUDPortMapping(CRUDBase[NATPortMapping, None, None]):
    async def get_by_x_ip_and_port(
        self,
        db: Session,
        timestamp_lt: datetime,
        timestamp_gt: datetime,
        x_ip: str = None,
        x_port: int = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[NATPortMapping]:
        filters = [
            NATPortMapping.timestamp.between(timestamp_gt, timestamp_lt),
        ]

        if x_ip is not None:
            filters.append(NATPortMapping.x_ip == x_ip)

        if x_port is not None:
            filters.append(NATPortMapping.x_port == x_port)

        query = select(NATPortMapping).where(*filters).limit(limit).offset(skip)
        results = await db.exec(query)

        return results.all()


port_mapping = CRUDPortMapping(NATPortMapping)
