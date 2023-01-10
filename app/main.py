import uvicorn as uvicorn
from fastapi import FastAPI
from api.api import api_router

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
