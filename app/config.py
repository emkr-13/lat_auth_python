from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config:
        env_file = ".env"

    @property
    def tortoise_config(self) -> dict:
        return {
            "connections": {"default": self.database_url},
            "apps": {
                "models": {
                    "models": ["app.models"],
                    "default_connection": "default",
                }
            },
        }

settings = Settings()
print(settings.tortoise_config)
print("Database URL:", settings.database_url)
print("Secret Key:", settings.secret_key)