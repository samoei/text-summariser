import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_app


def get_settings_override():
    return Settings(testing=True, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client
    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override()
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.model"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_app:
        yield test_app
