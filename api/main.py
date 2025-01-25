from fastapi import FastAPI

app = FastAPI()

from cgnec_api import views  # noqa: E402

app.include_router(views.api_router, prefix="/v1")
