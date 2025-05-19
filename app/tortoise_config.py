import os
from dotenv import load_dotenv

load_dotenv()

tortoise_config = {
    "connections": {"default": os.getenv("DATABASE_URL", "postgres://postgres:123@localhost:5432/lat_auth_python")},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    }
}