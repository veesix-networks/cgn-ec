from datetime import datetime
from sqlmodel import select, Session

from cgnec_api.crud.base import CRUDBase
from cgnec_api.models import NATAddressMapping


class CRUDAddressMapping(CRUDBase[NATAddressMapping, None, None]):
    async def get_by_x_ip(
        self,
        db: Session,
        timestamp_lt: datetime,
        timestamp_gt: datetime,
        x_ip: str = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[NATAddressMapping]:
        filters = [
            NATAddressMapping.timestamp.between(timestamp_gt, timestamp_lt),
        ]

        if x_ip is not None:
            filters.append(NATAddressMapping.x_ip == x_ip)

        query = select(NATAddressMapping).where(*filters).limit(limit).offset(skip)
        results = await db.exec(query)

        return results.all()


address_mapping = CRUDAddressMapping(NATAddressMapping)
