from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers import auth, users
from config import settings

app = FastAPI()

# Registrasi router
app.include_router(auth.router)
app.include_router(users.router)

# Konfigurasi Tortoise ORM
register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}