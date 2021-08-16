import os
import shutil
from typing import Generator

from fastapi import APIRouter
from fastapi import Depends, BackgroundTasks
from fastapi.responses import StreamingResponse

from app import schemas
from app.core import config
from app.api import deps
from app.api.deps import Permission


router = APIRouter()


def remove_file(path: str) -> None:
    os.unlink(path)


def iterfile(file_path: str) -> Generator:
    with open(file_path, mode="rb") as file:
        yield from file


@router.get("/files/{filename}")
async def download_file(
    filename: str,
    query: schemas.DownloadQuery = Permission("submit", schemas.DownloadQuery),
    settings: config.Settings = Depends(deps.get_settings),
) -> StreamingResponse:
    file_path = f"{settings.FILE_ROOT_PATH}/{query.base_dir}/{filename}"
    return StreamingResponse(iterfile(file_path))


@router.get("/files")
def download_zipped_folder(
    background_tasks: BackgroundTasks,
    query: schemas.DownloadQuery = Permission("submit", schemas.DownloadQuery),
    settings: config.Settings = Depends(deps.get_settings),
) -> StreamingResponse:
    shutil.make_archive(
        f"{settings.FILE_ROOT_PATH}/tmp/{query.zip_filename}",
        "zip",
        root_dir=settings.FILE_ROOT_PATH,
        base_dir=query.base_dir,
    )
    zip_file_path = f"{settings.FILE_ROOT_PATH}/tmp/{query.zip_filename}.zip"
    # you might wanna store it for caching, but details are left to implement
    background_tasks.add_task(remove_file, zip_file_path)
    return StreamingResponse(iterfile(zip_file_path), media_type="application/zip")


@router.get("/info", response_model=schemas.UserFromDB)
async def get_info(
    current_user: schemas.UserInDB = Depends(deps.get_current_active_user),
) -> schemas.UserInDB:
    return current_user
