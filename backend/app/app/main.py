from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config
from app.core.config import settings
from app.api.v1.api import router as v1_router


def create_app(settings: config.Settings) -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_STR)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8000",
            "http://localhost:3000",
            "http://localhost:9528"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # instead of include_router, so to separate differnt versions
    app.include_router(v1_router)

    @app.get("/status")
    def read_api_status() -> Dict[str, str]:
        return {"status": "OK"}

    return app


app = create_app(settings)


# in case it is needed
# @app.on_event('startup')
# async def startup() -> None:
#    pass
#
#
# @app.on_event('shutdown')
# async def shutdown() -> None:
#    pass
