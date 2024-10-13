from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
