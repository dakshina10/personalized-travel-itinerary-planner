from pydantic import BaseModel, Field
from typing import Optional

class TripRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=100)
    start_date: str
    end_date: str
    budget: float = Field(gt=0)
    currency: str = "INR"
    travel_style: str = "Balanced"
    interests: list[str] = Field(default_factory=list)
    group_size: int = Field(default=1, ge=1, le=30)
    pace: str = "Moderate"
    accommodation: str = "Any"
    notes: str = ""

class Activity(BaseModel):
    time: str
    title: str
    description: str
    category: str
    estimated_cost: float = 0
    transport: str = ""

class ItineraryDay(BaseModel):
    day: int
    date: str
    theme: str
    activities: list[Activity]

class Itinerary(BaseModel):
    id: str
    destination: str
    start_date: str
    end_date: str
    budget: float
    currency: str
    travel_style: str
    group_size: int
    summary: str
    days: list[ItineraryDay]
    estimated_total: float
    tips: list[str] = Field(default_factory=list)
    ai_generated: bool = False
    created_at: str

class UpdateTripRequest(BaseModel):
    itinerary: Itinerary
