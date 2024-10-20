from model.organization.content.course_model import Section
from repository.organization.content.section.section_repository import SectionRepository


class SectionService:
    def __init__(self, section_repository: SectionRepository):
        self.section_repository = section_repository

    async def create_section(self, section_data: Section) -> str:
        return await self.section_repository.create_section(section_data)

    async def get_sections(self, course_id: str):
        return await self.section_repository.get_sections_by_course_id(course_id)

    async def update_section(self, section_id: str, section_data: Section):
        await self.section_repository.update_section(section_id, section_data)

    async def delete_section(self, section_id: str):
        await self.section_repository.delete_section(section_id)
