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
                    "models": ["app.models"],  # Sesuaikan dengan lokasi model Anda
                    "default_connection": "default",
                }
            },
        }
        
print("Loading settings...")
settings = Settings()
print(f"Database URL: {settings.database_url}")
print(f"Secret Key: {settings.secret_key}")

settings = Settings()