from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import PostgresDsn
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

from app.main import app
from app.shared.dependencies import get_session


def get_test_db_url() -> str:
    return str(
        PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host="postgres-test",
            port=settings.POSTGRES_PORT,
            path=settings.POSTGRES_DB,
        )
    )


engine = create_engine(get_test_db_url(), echo=False)


@pytest.fixture
def session() -> Generator[Session]:
    """Sesión de base de datos."""
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db_session:
        yield db_session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client(session: Session) -> Generator[TestClient]:
    """Cliente FastAPI con sobrescritura de dependencias."""
    app.dependency_overrides[get_session] = lambda: session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
