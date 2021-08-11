from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_v1


def create_app() -> FastAPI:
    # to generate links to other docs at /api/docs
    tags_metadata = [
        {
            'name': 'v1',
            "description": "API version 1, check link on the right",
            'externalDocs': {
                'description': 'sub-docs',
                'url': 'http://127.0.0.1/api/v1/docs'
            }
        },
    ]
    
    app = FastAPI(root_path=settings.ROOT_STR, openapi_tags=tags_metadata)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost:8000',
            'http://localhost:3000',
            'http://localhost:9528'
            ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # instead of include_router, so to separate differnt versions
    app.mount(settings.API_V1_STR, api_v1)

    @app.get("/status")
    def read_api_status():
        return {"status": "OK"}

    return app


app = create_app()


# in case it is needed
#@app.on_event('startup')
#async def startup() -> None:
#    pass
#
#
#@app.on_event('shutdown')
#async def shutdown() -> None:
#    pass
