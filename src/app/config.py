import logging
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = float(
        1
    )  # does this in the background os.getenv("ENVIRONMENT", "dev")
    testing: bool = 0  # does this in the background os.getenv("TESTING", 0)
    database_url: AnyUrl = (
        None  # does this in the background os.getenv("DATABASE_URL", None)
    )


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment")
    return Settings()
