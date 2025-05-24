from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Festival(BaseModel):
    id: int
    name: str
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    contents: Optional[str] = None
    homepage: Optional[str] = None
    poster: Optional[str] = None
    created_at: Optional[datetime] = None

class QueryRequest(BaseModel):
    user_input: str
