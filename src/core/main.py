from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.core.config as config
from src.core.gql_schema import graphql_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await config.configure_app()

    yield

    # Shutdown
    pass


app = FastAPI(title="Hive API", description="An API for Collective Sensemaking", lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
