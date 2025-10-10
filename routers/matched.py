"""
Matched songs router for managing matched song-lyrics pairs.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from models import MatchedCreate, MatchedResponse, MatchedUpdate, MatchedWithDetails
from services.supabase_service import supabase_service

router = APIRouter()


@router.get("/", response_model=List[MatchedWithDetails])
async def get_matched_songs(
    q: str | None = Query(
        None,
        description="Search query for song title (partial match)",
    ),
    skip: int = Query(0, ge=0, description="Number of matched songs to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of matched songs to return")
):
    """Get all matched songs with pagination and optional title search."""
    try:
        matched_results = []
        if q:
            songs = await supabase_service.search_with_pattern("songs", "title", q, skip, limit)
            for song in songs:
                matches = await supabase_service.search("matched", {"song_id": song["id"]})
                for match in matches:
                    match_with_details = match.copy()
                    match_with_details["song"] = song
                    if match.get("lyrics_id"):
                        lyrics = await supabase_service.get("lyrics", match["lyrics_id"])
                        match_with_details["lyrics"] = lyrics
                    matched_results.append(match_with_details)
        return matched_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch matched songs: {str(e)}")

@router.get("/{matched_id}", response_model=MatchedWithDetails)
async def get_matched_song(matched_id: int):
    """Get a specific matched song by ID with full details."""
    try:
        matched_song = await supabase_service.get("matched", matched_id)
        if not matched_song:
            raise HTTPException(status_code=404, detail="Matched song not found")
        
        # Get related data
        if matched_song.get("song_id"):
            song = await supabase_service.get("songs", matched_song["song_id"])
            matched_song["song"] = song
        
        if matched_song.get("lyrics_id"):
            lyrics = await supabase_service.get("lyrics", matched_song["lyrics_id"])
            matched_song["lyrics"] = lyrics
        
        if matched_song.get("created_by_user_id"):
            user = await supabase_service.get("users", matched_song["created_by_user_id"])
            matched_song["created_by_user"] = user
        
        return matched_song
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch matched song: {str(e)}")


@router.post("/", response_model=MatchedResponse)
async def create_matched_song(matched_data: MatchedCreate):
    """Create a new matched song-lyrics pair."""
    try:
        matched_song = await supabase_service.create("matched", matched_data.model_dump())
        return matched_song
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create matched song: {str(e)}")


@router.put("/{matched_id}", response_model=MatchedResponse)
async def update_matched_song(matched_id: int, matched_data: MatchedUpdate):
    """Update a matched song."""
    matched_song = await supabase_service.get("matched", matched_id)
    if not matched_song:
        raise HTTPException(status_code=404, detail="Matched song not found")
    
    try:
        updated_matched_song = await supabase_service.update("matched", matched_id, matched_data.model_dump())
        return updated_matched_song
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update matched song: {str(e)}")


@router.delete("/{matched_id}")
async def delete_matched_song(matched_id: int):
    """Delete a matched song."""
    matched_song = await supabase_service.get("matched", matched_id)
    if not matched_song:
        raise HTTPException(status_code=404, detail="Matched song not found")
    
    try:
        success = await supabase_service.delete("matched", matched_id)
        if success:
            return {"message": "Matched song deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete matched song")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete matched song: {str(e)}")


@router.get("/search/existing")
async def search_existing_matched_songs(
    song_id: Optional[int] = Query(None, description="Filter by song ID"),
    lyrics_id: Optional[int] = Query(None, description="Filter by lyrics ID"),
    created_by_user_id: Optional[int] = Query(None, description="Filter by creator user ID")
):
    """Search for existing matched songs with optional filters."""
    try:
        filters = {}
        if song_id is not None:
            filters["song_id"] = song_id
        if lyrics_id is not None:
            filters["lyrics_id"] = lyrics_id
        if created_by_user_id is not None:
            filters["created_by_user_id"] = created_by_user_id
        
        matched_songs = await supabase_service.search("matched", filters)
        return matched_songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search matched songs: {str(e)}")
