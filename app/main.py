from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import players

app = FastAPI(
    title="Chess Stats API",
    description="API for accessing stats for chess player data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router, prefix="/api/v1", tags=["players"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Chess Stats API"}