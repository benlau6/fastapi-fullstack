from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import deps
from app.core.config import settings
from app.core import config
from app.api.v1.api import router as v1_router

test_file_root_path = '/data/test_files/'
test_mongo_db_name = 'test'
# ROOT_STR = '' because inside the container, there is no proxy, 
# then the original routes are mounted with no root str
test_config = config.Settings(MONGO_DB_NAME=test_mongo_db_name, ROOT_STR='', FILE_ROOT_PATH=test_file_root_path)


def get_settings_override():
    return test_config


def create_app(settings) -> FastAPI:    
    app = FastAPI(root_path=settings.ROOT_STR)

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
    app.include_router(v1_router)

    @app.get("/status")
    def read_api_status():
        return {"status": "OK"}

    return app


app = create_app(settings)


# in case it is needed
#@app.on_event('startup')
#async def startup() -> None:
#    pass
#
#
#@app.on_event('shutdown')
#async def shutdown() -> None:
#    pass
