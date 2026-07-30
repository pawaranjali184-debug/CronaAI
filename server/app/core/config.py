# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "CronaAI Server"

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    MYSQL_HOST: str = Field("127.0.0.1", env="MYSQL_HOST")
    MYSQL_PORT: int = Field(3306, env="MYSQL_PORT")
    MYSQL_USER: str = Field(..., env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(..., env="MYSQL_PASSWORD")
    MYSQL_DATABASE: str = Field(..., env="MYSQL_DATABASE")

    SMTP_HOST: str = Field("localhost", env="SMTP_HOST")
    SMTP_PORT: int = Field(1025, env="SMTP_PORT")
    SMTP_USER: str | None = Field(None, env="SMTP_USER")
    SMTP_PASSWORD: str | None = Field(None, env="SMTP_PASSWORD")
    EMAIL_FROM: str = Field("no-reply@cronaai.dev", env="EMAIL_FROM")

    FILE_UPLOAD_DIR: str = Field("uploads", env="FILE_UPLOAD_DIR")

    # ✅ Add this
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset=utf8mb4"
        )


settings = Settings()