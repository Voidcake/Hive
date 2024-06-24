from fastapi import FastAPI

from core.config import configure_app

app = FastAPI(title="Hive API", description="An API for Collective Sensemaking")


@app.on_event("startup")
async def startup_event():
    await configure_app()


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.get("/")
async def root():
    return {"message": "Hello World"}
