import io

import boto3
from fastapi import UploadFile, Depends
from config.enviroment.env_config import settings
from repository.organization.video.video_repository import VideoRepository, get_video_repository


class VideoService:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    async def upload_video(self, organization_id: str, course_id: str, file: UploadFile) -> str:
        file_path = f"{organization_id}/content/{course_id}/videos/{file.filename}"

        # Upload the file to AWS S3
        file_content = await file.read()  # Asynchronously read file contents
        self.s3_client.upload_fileobj(io.BytesIO(file_content), self.bucket_name, file_path,
                                      ExtraArgs={"ContentType": file.content_type})

        # Save video metadata in MongoDB using the repository
        video_data = {
            "organization_id": organization_id,
            "course_id": course_id,
            "file_path": file_path,
        }
        video_id = await self.video_repository.insert_video(video_data)

        return video_id



async def get_video_service(video_repository: VideoRepository = Depends(get_video_repository)) -> VideoService:
    return VideoService(video_repository)