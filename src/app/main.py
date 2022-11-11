import logging

from fastapi import FastAPI

from app.api import ping, summaries
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app_instance = FastAPI()

    app_instance.include_router(ping.router)
    app_instance.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"]
    )

    return app_instance


app = create_app()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
