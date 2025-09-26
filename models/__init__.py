"""
Pydantic schemas package for API.
"""
from .song import SongCreate, SongUpdate, SongResponse, SongInDB
from .lyrics import LyricsCreate, LyricsResponse, LyricsWithLines, LyricLineCreate, LyricLineResponse
from .user import UserCreate, UserUpdate, UserResponse, UserInDB, UserLogin, UserSignup
from .matched import MatchedCreate, MatchedUpdate, MatchedResponse, MatchedWithDetails, MatchedInDB
from .user_library import UserLibraryCreate, UserLibraryUpdate, UserLibraryResponse, UserLibraryWithDetails, UserLibraryInDB
from .user_progress import (
    UserProgressCreate, 
    UserProgressUpdate, 
    UserProgressResponse, 
    UserProgressWithDetails, 
    UserProgressInDB,
    PracticeSessionCreate,
    PracticeSessionResponse
)

__all__ = [
    # Song schemas
    "SongCreate", "SongUpdate", "SongResponse", "SongInDB",
    
    # Lyrics schemas
    "LyricsCreate", "LyricsResponse", "LyricsWithLines", 
    "LyricLineCreate", "LyricLineResponse",
    
    # User schemas
    "UserCreate", "UserUpdate", "UserResponse", "UserInDB", "UserLogin", "UserSignup",
    
    # Matched schemas
    "MatchedCreate", "MatchedUpdate", "MatchedResponse", "MatchedWithDetails", "MatchedInDB",
    
    # User Library schemas
    "UserLibraryCreate", "UserLibraryUpdate", "UserLibraryResponse", "UserLibraryWithDetails", "UserLibraryInDB",
    
    # User Progress schemas
    "UserProgressCreate", "UserProgressUpdate", "UserProgressResponse", 
    "UserProgressWithDetails", "UserProgressInDB", "PracticeSessionCreate", "PracticeSessionResponse",
]
