from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    version="1.0.0",
    description="AI-powered comic story creator using Gemini and Hugging Face.",
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


# Routes
app.include_router(router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "ComicCraft",
    }