from datetime import datetime
from ipaddress import IPv4Address
from sqlmodel import select, Session

from cgnec_api.crud.base import CRUDBase
from cgnec_api.models import NATSessionMapping


class CRUDSessionMapping(CRUDBase[NATSessionMapping, None, None]):
    async def get_by_x_ip(
        self,
        db: Session,
        timestamp_lt: datetime,
        timestamp_gt: datetime,
        x_ip: str = None,
        x_port: int = None,
        dst_ip: str = None,
        dst_port: int = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[NATSessionMapping]:
        filters = [
            NATSessionMapping.timestamp <= timestamp_lt,
            NATSessionMapping.timestamp >= timestamp_gt,
        ]

        if x_ip is not None:
            filters.append(NATSessionMapping.x_ip == IPv4Address(x_ip))

        if x_port is not None:
            filters.append(NATSessionMapping.x_port == int(x_port))

        if dst_ip is not None:
            filters.append(NATSessionMapping.dst_ip == IPv4Address(dst_ip))

        if dst_port is not None:
            filters.append(NATSessionMapping.dst_port == int(dst_port))

        query = select(NATSessionMapping).where(*filters).limit(limit).offset(skip)
        results = await db.exec(query)

        return results.all()


session_mapping = CRUDSessionMapping(NATSessionMapping)
