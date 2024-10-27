from db.mongo.sync_connection.connection.pymongo_connection import get_sync_connection
from repository.organization.video.video_repository import  VideoRepository
from service.organization.content.video.video_service import VideoService
from service.s3.config.s3_config import get_s3_config
from service.s3.s3_service import S3Service


class VideoServiceFactory:
    @staticmethod
    def create():
        db = get_sync_connection()
        video_repository = VideoRepository(db)
        s3_service = S3Service(get_s3_config())

        return VideoService(s3_service, video_repository)

