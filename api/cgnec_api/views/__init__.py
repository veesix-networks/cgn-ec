from fastapi import APIRouter

api_router = APIRouter()

from cgnec_api.views import address_mappings  # noqa: E402
from cgnec_api.views import port_block_mappings  # noqa: E402
from cgnec_api.views import port_mappings  # noqa: E402
from cgnec_api.views import session_mappings  # noqa: E402
from cgnec_api.views import deterministic_nat  # noqa: E402

api_router.include_router(address_mappings.router, prefix="/address_mappings")
api_router.include_router(port_block_mappings.router, prefix="/port_block_mappings")
api_router.include_router(port_mappings.router, prefix="/port_mappings")
api_router.include_router(session_mappings.router, prefix="/session_mappings")
api_router.include_router(deterministic_nat.router, prefix="/deterministic_nat")
