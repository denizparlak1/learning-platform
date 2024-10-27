from datetime import datetime
from fastapi import Depends, HTTPException

from model.organization.content.course_model import Video
from repository.organization.video.video_repository import VideoRepository, get_video_repository
from service.s3.s3_service import S3Service, get_s3_service


class VideoService:
    def __init__(self, s3_service: S3Service, video_repository: VideoRepository):
        self.s3_service = s3_service
        self.video_repository = video_repository

    def upload_video_to_s3(self, organization_id, course_id, file_content, filename, content_type,is_public,section_id):
        file_path = f"{organization_id}/content/{course_id}/videos/section/{section_id}/{filename}"
        uploaded_file_path = self.s3_service.upload_file(file_path, file_content, content_type)

        video_data = {
            "organization_id": organization_id,
            "course_id": course_id,
            "section_id":section_id,
            "file_path": file_path,
            "content_type": content_type,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_public":is_public
        }

        self.video_repository.insert_video(video_data)

        return uploaded_file_path

    async def get_videos_by_section_id(self, section_id: str) -> Video:
        return await self.video_repository.get_videos_by_section_id(section_id)

    async def delete_video(self, video_id: str) -> bool:
        video_data = await self.video_repository.get_video_by_id(video_id)
        if not video_data:
            raise HTTPException(status_code=404, detail="Video not found")
        self.s3_service.delete_file(video_data['file_path'])
        return await self.video_repository.delete_video(video_id)

def get_video_service(s3_service: S3Service = Depends(get_s3_service),
                       video_repository: VideoRepository = Depends(get_video_repository)) -> VideoService:
    return VideoService(s3_service, video_repository)
