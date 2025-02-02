from fastapi import FastAPI, Depends
from cgnec_api.dependencies import require_local_api_key

app = FastAPI(
    title="cgn-ec",
    description="Flexible solution for your CGNAT logging needs",
    dependencies=[Depends(require_local_api_key)],
)

from cgnec_api import views  # noqa: E402

app.include_router(views.api_router, prefix="/v1")
