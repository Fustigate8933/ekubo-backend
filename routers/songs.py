from fastapi import APIRouter, HTTPException, Query

from services.song_service import fetch_lyrics, generate_spotify_tracks

router = APIRouter()


@router.get("/lyrics")
async def get_lyrics(
    q: str | None = Query(
        None,
        description="Search query for keyword in ANY field such as artist or track name",
    ),
):
    if not q:
        raise HTTPException(
            status_code=400,
            detail="Both 'track_name' and 'artist_name' cannot be missing. Provide at least one.",
        )

    try:
        lyrics_data = await fetch_lyrics(q)
        return lyrics_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred."
        ) from e


@router.get("/spotify-tracks")
async def get_spotify_tracks(
    track_name: str = Query(..., description="Track name"),
    artist_name: str = Query(..., description="Artist name"),
    track_limit: int = Query(1, description="Number of tracks to return")
):
    try:
        tracks = await generate_spotify_tracks(track_name, artist_name, track_limit)
        return {"tracks": tracks}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred."
        ) from e
