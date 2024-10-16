from postmarker.core import PostmarkClient
from config.enviroment.env_config import settings


class PostmarkService:
    def __init__(self):
        """Initialize the Postmark client with server token from settings."""
        self.client = PostmarkClient(server_token=settings.POSTMARK_SERVER_TOKEN)
        self.from_address = settings.EMAIL_FROM  # Sender email address from settings


    async def send_with_template(self, to_address: str, template_id: int, template_model: dict):
        """Send an email using a Postmark template."""
        try:
            self.client.emails.send_with_template(
                From=self.from_address,
                To=to_address,
                TemplateId=template_id,
                TemplateModel=template_model
            )
        except Exception as e:
            raise

async def get_postmark_service() -> PostmarkService:
    postmark_service = PostmarkService()
    return postmark_service