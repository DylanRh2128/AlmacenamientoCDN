from fastapi import FastAPI

from app.db import Base, engine
from app import models  # noqa: F401 — registers models on Base before create_all
from app.files import router as files_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Private File Storage API")
app.include_router(files_router)


@app.get("/health")
def health():
    return {"status": "ok"}
