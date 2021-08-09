import os
import shutil

from fastapi import APIRouter
from fastapi import Depends, BackgroundTasks
from fastapi.responses import StreamingResponse 

from app import schemas
from app.core import config
from app.api import deps
from app.api.fastapi_permissions_utils import Permission


router = APIRouter()


def remove_file(path: str) -> None:
    os.unlink(path)


@router.get("/files/{filename}")
async def download_file(
    filename: str,
    query: schemas.DownloadQuery = Permission('submit', schemas.DownloadQuery),
    settings: config.Settings = Depends(deps.get_settings)
    ):
    file_path = f'{settings.FILE_ROOT_PATH}/{query.base_dir}/{filename}'
    def iterfile():  
        with open(file_path, mode="rb") as file:  
            yield from file  
    return StreamingResponse(iterfile())


@router.get("/files")
def download_zipped_folder(
    background_tasks: BackgroundTasks,
    query: schemas.DownloadQuery = Permission('submit', schemas.DownloadQuery),
    settings: config.Settings = Depends(deps.get_settings)
    ):
    shutil.make_archive(f'{settings.FILE_ROOT_PATH}/tmp/{query.zip_filename}', 'zip', root_dir=settings.FILE_ROOT_PATH, base_dir=query.base_dir)
    zip_file_path = f'{settings.FILE_ROOT_PATH}/tmp/{query.zip_filename}.zip'
    def iterfile():  
        with open(zip_file_path, mode="rb") as file:  
            yield from file  
    # you might wanna store it for caching, but details are left to implement
    background_tasks.add_task(remove_file, zip_file_path)
    return StreamingResponse(iterfile(), media_type='application/zip')


@router.get("/info", response_model=schemas.User)
async def get_info(current_user: schemas.User = Depends(deps.get_current_active_user)):
    return current_user
