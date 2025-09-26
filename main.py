from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import songs, auth, songs_new, lyrics, matched, user_library

app = FastAPI(
    title="Ekubo API",
    description="Japanese listening practice API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Legacy routes (for backward compatibility)
app.include_router(songs.router, prefix="/songs", tags=["Songs (Legacy)"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# New enhanced routes
app.include_router(songs_new.router, prefix="/api/songs", tags=["Songs"])
app.include_router(lyrics.router, prefix="/api/lyrics", tags=["Lyrics"])
app.include_router(matched.router, prefix="/api/matched", tags=["Matched Songs"])
app.include_router(user_library.router, prefix="/api/library", tags=["User Library"])
