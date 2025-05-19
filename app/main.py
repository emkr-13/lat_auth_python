from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers import auth, users
from app.config import settings
from app.tortoise_config import tortoise_config

app = FastAPI()

# Registrasi router
app.include_router(auth.router)
app.include_router(users.router)

# Konfigurasi Tortoise ORM
register_tortoise(
    app,
    config=tortoise_config,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}