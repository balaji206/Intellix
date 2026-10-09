from fastapi import FastAPI

from app.routes import health

app = FastAPI(title="Intellix RAG Service")

app.include_router(health.router)