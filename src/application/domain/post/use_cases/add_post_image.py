from uuid import uuid4
import shutil
import os

from fastapi import UploadFile, File
from application.schemas.posts import PostImageResponse
from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
)


class AddPostImageUseCase:
    def __init__(self) -> None:
        self.image_folder = 'static/images'
        os.makedirs(self.image_folder, exist_ok=True)

    async def execute(self, image: UploadFile) -> PostImageResponse:
        extension = image.filename.split('.')[-1].lower()
        if extension not in ('jpeg', 'jpg', 'png'):
            raise UploadFileIsNotImageException()

        new_image_name: str = str(uuid4())
        new_image_path: str = (
            f'{self.image_folder}/{new_image_name}.{extension}'
        )

        with open(new_image_path, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)

        return PostImageResponse(
            image_path=f'/static/images/{new_image_name}.{extension}'
        )
