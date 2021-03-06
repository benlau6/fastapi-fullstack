from typing import List
import os
import shutil

import asyncio
from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks

from app import schemas
from app.core import config
from app.api import deps
from app.api.deps import Permission


router = APIRouter()


def write_file_to_local(
    form: schemas.UploadForm, file: UploadFile, settings: config.Settings
) -> None:
    file_dir = f"{settings.FILE_ROOT_PATH}/{form.base_dir}"
    file_path = f"{file_dir}/{file.filename}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


@router.post(
    "/files",
    dependencies=[Depends(deps.verify_content_length)],
    response_model=schemas.UploadRecords,
)
async def upload_files(
    files: List[UploadFile] = File(...),
    form: schemas.UploadForm = Permission("submit", schemas.UploadForm.as_form),
    current_user: schemas.UserInDB = Depends(deps.get_current_active_user),
    settings: config.Settings = Depends(deps.get_settings),
    *,
    background_tasks: BackgroundTasks,
) -> schemas.UploadRecords:
    async def copy_file(file: UploadFile) -> schemas.UploadRecord:
        background_tasks.add_task(write_file_to_local, form, file, settings)

        record = schemas.UploadRecord(
            filename=file.filename,
            # file_size=file.file.tell(), # its not working, needa read all to return actual size, but it slow down the processing, which now put to background
            file_content_type=file.content_type,
            owner=current_user["email"],
        )
        return record

    record_list = await asyncio.gather(*map(copy_file, files))
    records = schemas.UploadRecords(records=record_list)
    return records


@router.get("/info", response_model=schemas.UserFromDB)
async def get_info(
    current_user: schemas.UserInDB = Depends(deps.get_current_active_user),
) -> schemas.UserInDB:
    return current_user
