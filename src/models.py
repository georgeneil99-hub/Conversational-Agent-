from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserProfile(BaseModel):
    """Stores persistent user profile data"""
    name: str = Field(..., example="Ritika")
    birth_date: str = Field(..., example="1995-08-20") # format: YYYY-MM-DD
    birth_time: str = Field(..., example="14:30")
    birth_place: str = Field(..., example="Jaipur, India")
    preferred_language: str = Field(default="en", example="hi")

class ChatRequest(BaseModel):
    """Input structure for the /chat POST endpoint"""
    session_id: str = Field(..., example="abc-123")
    message: str = Field(..., example="How will my month be in career?")
    user_profile: UserProfile

class ChatResponse(BaseModel):
    """Output structure following the assignment's stricter semantics"""
    response: str
    zodiac: str
    context_used: List[str]
    retrieval_used: bool

def calculate_zodiac(birth_date: str) -> str:
    """Mandatory helper to derive the Zodiac sign from the profile."""
    try:
        date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
        month = date_obj.month
        day = date_obj.day
        
        if (month == 12 and day >= 22) or (month == 1 and day <= 19): return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "Aquarius"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20): return "Pisces"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19): return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "Sagittarius"
    except Exception:
        return "Unknown"
    return "Unknown"