from fastapi import Depends
from model.organization.content.course_model import Section
from repository.organization.content.section.section_repository import SectionRepository, get_section_repository
from repository.organization.video.video_repository import VideoRepository, get_video_repository
from service.s3.s3_service import S3Service, get_s3_service


class SectionService:
    def __init__(self, section_repository: SectionRepository, video_repository: VideoRepository,s3_service: S3Service):
        self.section_repository = section_repository
        self.video_repository = video_repository
        self.s3_service = s3_service

    async def create_section(self, section_data: Section) -> str:
        return await self.section_repository.create_section(section_data)

    async def get_sections(self, course_id: str) -> Section:
        return await self.section_repository.get_sections_by_course_id(course_id)

    async def update_section(self, section_id: str, section_data: Section):
        await self.section_repository.update_section(section_id, section_data)


    async def delete_section_with_content(self, section_id: str) -> bool:
        section = await self.section_repository.get_section_by_id(section_id)
        s3_prefix = f"{section.organization_id}/content/{section.course_id}/videos/section/{section_id}/"
        self.s3_service.delete_files_by_prefix(s3_prefix)

        videos_deleted = await self.video_repository.delete_videos_by_section_id(section_id)
        section_deleted = await self.section_repository.delete_section(section_id)
        return videos_deleted and section_deleted

def get_section_service(section_repository: SectionRepository = Depends(get_section_repository),
                        video_repository: VideoRepository = Depends(get_video_repository),
                        s3_service: S3Service = Depends(get_s3_service)) -> SectionService:
    return SectionService(section_repository, video_repository,s3_service)
