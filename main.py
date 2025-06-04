import uvicorn
from fastapi import FastAPI

from setting import settings
from routes import router

app = FastAPI(title="API для администрирования пользователей", version="0.0.1")
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )