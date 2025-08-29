from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import songs, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(songs.router, prefix="/songs", tags=["Songs"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
