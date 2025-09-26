"""
Enhanced songs router for managing songs.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from models import SongCreate, SongResponse, SongUpdate
from services.supabase_service import supabase_service

router = APIRouter()


@router.get("/", response_model=List[SongResponse])
async def get_songs(
    skip: int = Query(0, ge=0, description="Number of songs to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of songs to return"),
    title: Optional[str] = Query(None, description="Filter by song title"),
    artist: Optional[str] = Query(None, description="Filter by artist name")
):
    """Get all songs with pagination and optional filters."""
    try:
        filters = {}
        if title:
            filters["title"] = title
        if artist:
            filters["artist"] = artist
        
        if filters:
            songs = await supabase_service.search("songs", filters, skip=skip, limit=limit)
        else:
            songs = await supabase_service.get_multi("songs", skip=skip, limit=limit)
        return songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch songs: {str(e)}")


@router.get("/{song_id}", response_model=SongResponse)
async def get_song(song_id: int):
    """Get a specific song by ID."""
    try:
        song = await supabase_service.get("songs", song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        return song
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch song: {str(e)}")


@router.post("/", response_model=SongResponse)
async def create_song(song_data: SongCreate):
    """Create a new song."""
    try:
        song = await supabase_service.create("songs", song_data.model_dump())
        return song
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create song: {str(e)}")


@router.put("/{song_id}", response_model=SongResponse)
async def update_song(song_id: int, song_data: SongUpdate):
    """Update a song."""
    song = await supabase_service.get("songs", song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    try:
        updated_song = await supabase_service.update("songs", song_id, song_data.model_dump())
        return updated_song
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update song: {str(e)}")


@router.delete("/{song_id}")
async def delete_song(song_id: int):
    """Delete a song."""
    song = await supabase_service.get("songs", song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    try:
        success = await supabase_service.delete("songs", song_id)
        if success:
            return {"message": "Song deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete song")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete song: {str(e)}")
