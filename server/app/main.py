from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import auth, users, ai, activity
from app.core.database import engine, Base
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="CronaAI development backend API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://crona-ai-ygq1.vercel.app",
    ]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])
app.include_router(activity.router, prefix="/api/v1/activity", tags=["Activity"])


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/api/v1/health")
async def health_check() -> dict:
    return {"status": "ok", "message": "CronaAI backend is running"}
