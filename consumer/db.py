from sqlalchemy.schema import CreateTable
from consumer.models import (
    NATAddressMapping,
    NATPortBlockMapping,
    NATPortMapping,
    NATSessionMapping,
)

print(CreateTable(NATAddressMapping.__table__))
print(CreateTable(NATPortBlockMapping.__table__))
print(CreateTable(NATPortMapping.__table__))
print(CreateTable(NATSessionMapping.__table__))
