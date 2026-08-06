import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401 — registers models on Base before create_all
from app.db import Base, get_db
from app.main import app

API_KEY = "test-api-key"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("API_KEY", API_KEY)

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr("app.files.upload_file", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.files.delete_file", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "app.files.generate_download_url", lambda s3_key, **kwargs: f"https://fake.cdn/{s3_key}"
    )

    yield TestClient(app)

    app.dependency_overrides.clear()
