from pydantic import BaseModel
from typing import Optional

class Song(BaseModel):
    id: str
    title: str
    artist: str
    lyrics: Optional[str] = None
