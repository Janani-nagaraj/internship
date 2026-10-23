from fastapi import FastAPI

from routes import final, home, report0

app = FastAPI(
    title="Document Verification API",
    description="Upload documents once and verify them automatically",
    version="4.0",
)

app.include_router(home.router)
app.include_router(report0.router)
app.include_router(final.router)
