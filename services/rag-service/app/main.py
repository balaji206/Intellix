from fastapi import FastAPI

from app.routes import documents, health

app = FastAPI(title="Intellix RAG Service")
app.include_router(health.router)
app.include_router(documents.router)