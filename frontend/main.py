from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
#from app.api.v1.api import router as api_v1_router


templates = Jinja2Templates(directory="templates")

def create_app() -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_STR)

    app.mount("/sdk", StaticFiles(directory="templates/sdk"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #app.include_router(api_v1_router, prefix=settings.API_V1_STR)


    @app.get("/status")
    def read_api_status():
        return {"status": "OK"}

    @app.get("/login")
    async def login(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    return app

app = create_app()


# just for dev
@app.on_event('startup')
async def startup() -> None:
    pass


@app.on_event('shutdown')
async def shutdown() -> None:
    pass
