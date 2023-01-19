import uvicorn as uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.api import api_router
from core.config import get_settings
from db import get_session

settings = get_settings()

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def startup():
    get_session.engine = create_async_engine(settings.postgres_dsn)
    get_session.sql_session = sessionmaker(
        get_session.engine, class_=AsyncSession
    )


@app.on_event("shutdown")
async def shutdown():
    await get_session.engine.dispose()


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
