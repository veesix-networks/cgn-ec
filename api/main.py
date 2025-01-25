from fastapi import FastAPI

app = FastAPI(
    title="cgn-ec", description="Flexible solution for your CGNAT logging needs"
)

from cgnec_api import views  # noqa: E402

app.include_router(views.api_router, prefix="/v1")
