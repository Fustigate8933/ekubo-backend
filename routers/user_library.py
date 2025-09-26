"""
User Library router for managing user's song library.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from models import UserLibraryCreate, UserLibraryResponse, UserLibraryUpdate, UserLibraryWithDetails
from services.supabase_service import supabase_service

router = APIRouter()


@router.get("/", response_model=List[UserLibraryResponse])
async def get_user_libraries(
    skip: int = Query(0, ge=0, description="Number of library entries to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of library entries to return")
):
    """Get all user library entries with pagination."""
    try:
        library_entries = await supabase_service.get_multi("user_library", skip=skip, limit=limit)
        return library_entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user library entries: {str(e)}")


@router.get("/user/{user_id}", response_model=List[UserLibraryWithDetails])
async def get_user_library(user_id: int):
    """Get a specific user's library with full details."""
    try:
        library_entries = await supabase_service.search("user_library", {"user_id": user_id})
        
        # Get full details for each entry
        detailed_entries = []
        for entry in library_entries:
            if entry.get("matched_song_id"):
                matched_song = await supabase_service.get("matched", entry["matched_song_id"])
                if matched_song:
                    # Get song and lyrics details
                    if matched_song.get("song_id"):
                        song = await supabase_service.get("songs", matched_song["song_id"])
                        matched_song["song"] = song
                    
                    if matched_song.get("lyrics_id"):
                        lyrics = await supabase_service.get("lyrics", matched_song["lyrics_id"])
                        matched_song["lyrics"] = lyrics
                    
                    entry["matched_song"] = matched_song
            
            if entry.get("user_id"):
                user = await supabase_service.get("users", entry["user_id"])
                entry["user"] = user
            
            detailed_entries.append(entry)
        
        return detailed_entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user library: {str(e)}")


@router.get("/{library_id}", response_model=UserLibraryWithDetails)
async def get_library_entry(library_id: int):
    """Get a specific library entry by ID with full details."""
    try:
        library_entry = await supabase_service.get("user_library", library_id)
        if not library_entry:
            raise HTTPException(status_code=404, detail="Library entry not found")
        
        # Get matched song details
        if library_entry.get("matched_song_id"):
            matched_song = await supabase_service.get("matched", library_entry["matched_song_id"])
            if matched_song:
                # Get song and lyrics details
                if matched_song.get("song_id"):
                    song = await supabase_service.get("songs", matched_song["song_id"])
                    matched_song["song"] = song
                
                if matched_song.get("lyrics_id"):
                    lyrics = await supabase_service.get("lyrics", matched_song["lyrics_id"])
                    matched_song["lyrics"] = lyrics
                
                library_entry["matched_song"] = matched_song
        
        # Get user details
        if library_entry.get("user_id"):
            user = await supabase_service.get("users", library_entry["user_id"])
            library_entry["user"] = user
        
        return library_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch library entry: {str(e)}")


@router.post("/", response_model=UserLibraryResponse)
async def add_to_library(library_data: UserLibraryCreate):
    """Add a song to user's library."""
    try:
        # Check if the entry already exists
        existing_entries = await supabase_service.search("user_library", {
            "user_id": library_data.user_id,
            "matched_song_id": library_data.matched_song_id
        })
        
        if existing_entries:
            raise HTTPException(status_code=400, detail="Song already in library")
        
        library_entry = await supabase_service.create("user_library", library_data.model_dump())
        return library_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to library: {str(e)}")


@router.put("/{library_id}", response_model=UserLibraryResponse)
async def update_library_entry(library_id: int, library_data: UserLibraryUpdate):
    """Update a library entry."""
    library_entry = await supabase_service.get("user_library", library_id)
    if not library_entry:
        raise HTTPException(status_code=404, detail="Library entry not found")
    
    try:
        updated_entry = await supabase_service.update("user_library", library_id, library_data.model_dump())
        return updated_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update library entry: {str(e)}")


@router.delete("/{library_id}")
async def remove_from_library(library_id: int):
    """Remove a song from user's library."""
    library_entry = await supabase_service.get("user_library", library_id)
    if not library_entry:
        raise HTTPException(status_code=404, detail="Library entry not found")
    
    try:
        success = await supabase_service.delete("user_library", library_id)
        if success:
            return {"message": "Song removed from library successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to remove from library")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove from library: {str(e)}")
