from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    api_key: str | None = Field(default=None, alias="API_KEY")
    admin_password: str | None = Field(default=None, alias="ADMIN_PASSWORD")

    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")

    aws_region: str = Field(alias="AWS_REGION")
    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    s3_bucket: str = Field(alias="S3_BUCKET")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")

    model_config = {
        "env_file": os.getenv("ENV_FILE", "backend/.env"),
        "extra": "ignore",
        "env_file_encoding": "utf-8",
    }


settings = Settings()  # type: ignore[call-arg]
