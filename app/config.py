from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    app_port: int = 4000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()