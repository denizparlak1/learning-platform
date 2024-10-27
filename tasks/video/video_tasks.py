import logging
from config.celery.celery_config import celery_app
from service.organization.content.video.factory.video_factory import VideoServiceFactory


@celery_app.task
def upload_video_to_s3_task(organization_id, course_id, file_content, filename, content_type,is_public,section_id):
    try:
        video_service = VideoServiceFactory.create()
        uploaded_file_path = video_service.upload_video_to_s3(organization_id, course_id, file_content, filename, content_type,is_public,section_id)

        return uploaded_file_path
    except Exception as e:
        logging.error(f"Error during video upload: {e}")
        raise
