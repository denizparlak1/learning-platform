from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    POSTMARK_SERVER_TOKEN:str
    EMAIL_FROM:str
    POSTMARK_WELCOME_TEMPLATE_ID:str
    POSTMARK_RESET_PASSWORD_TEMPLATE:str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_REGION: str
    class Config:
        env_file = ".env"

settings = Settings()
