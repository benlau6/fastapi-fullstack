from typing import List

from fastapi import APIRouter

from app import schemas

from fastapi import Depends, Security, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse 

from fastapi.templating import Jinja2Templates

from app.core import config
from app.api import deps
import os
import shutil
from app.core.config import settings


router = APIRouter()

scopes = settings.SCOPES_DOWNLOAD

templates = Jinja2Templates(directory="/app/app/templates")


def remove_file(path: str) -> None:
    os.unlink(path)


@router.get("/files/{filename}")
async def download_file(
    filename: str,
    form: schemas.DownloadForm = Depends(schemas.DownloadForm.as_form),
    current_user: schemas.User = Depends(deps.get_current_active_user),
    settings: config.Settings = Depends(deps.get_settings)
    ):
    file_path = f'{settings.FILE_ROOT_PATH}/{form.base_dir}/{filename}'
    def iterfile():  
        with open(file_path, mode="rb") as file:  
            yield from file  
    return StreamingResponse(iterfile())


@router.get("/files")
def download_zipped_folder(
    background_tasks: BackgroundTasks,
    form: schemas.DownloadForm = Depends(schemas.DownloadForm.as_form),
    current_user: schemas.User = Depends(deps.get_current_active_user),
    settings: config.Settings = Depends(deps.get_settings)
    ):
    shutil.make_archive(f'{settings.FILE_ROOT_PATH}/tmp/{form.zip_filename}', 'zip', root_dir=settings.FILE_ROOT_PATH, base_dir=form.base_dir)
    zip_file_path = f'{settings.FILE_ROOT_PATH}/tmp/{form.zip_filename}.zip'
    def iterfile():  
        with open(zip_file_path, mode="rb") as file:  
            yield from file  
    # you might wanna store it for caching, but details are left to implement
    background_tasks.add_task(remove_file, zip_file_path)
    return StreamingResponse(iterfile(), media_type='application/zip')


@router.get("/info")
async def get_info(current_user: schemas.User = Depends(deps.get_current_active_user)):
    return current_user
