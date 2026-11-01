import json, uuid
from datetime import date, timedelta, datetime, timezone
import httpx
from .config import settings
from .models import TripRequest, Itinerary

SYSTEM_PROMPT = '''You are a careful travel-planning assistant. Return ONLY valid JSON matching:
{"summary":"...","days":[{"day":1,"date":"YYYY-MM-DD","theme":"...","activities":[{"time":"09:00","title":"...","description":"...","category":"Attraction|Food|Stay|Transport|Experience","estimated_cost":500,"transport":"..."}]}],"estimated_total":1000,"tips":["..."]}
Create a practical day-wise plan. Keep costs within the user's total budget where possible. Include meals, local transport notes, and accommodation suggestions when relevant. Do not claim live availability or guaranteed opening hours. Use reasonable estimates and disclose uncertainty in tips.'''

def demo_plan(req: TripRequest, dates: list[date]) -> dict:
    interests = ", ".join(req.interests) if req.interests else "local highlights"
    days = []
    per_day = max(req.budget / max(len(dates), 1), 0)
    for idx, day in enumerate(dates, 1):
        days.append({
            "day": idx, "date": day.isoformat(),
            "theme": ["Explore the city", "Local culture and flavours", "Relax and discover"][min(idx-1, 2)],
            "activities": [
                {"time":"08:30","title":"Breakfast at a local cafe","description":"Start with a locally popular breakfast option. Check current timings before visiting.","category":"Food","estimated_cost":round(per_day*.10,2),"transport":"Walk or short local cab ride."},
                {"time":"10:00","title":f"Explore a signature attraction in {req.destination}","description":f"Choose a well-reviewed landmark related to {interests}. Verify entry rules and opening hours.","category":"Attraction","estimated_cost":round(per_day*.22,2),"transport":"Use public transport or a cab; group travel may reduce per-person cost."},
                {"time":"13:00","title":"Regional lunch experience","description":"Try a popular regional dish at a restaurant that matches your budget.","category":"Food","estimated_cost":round(per_day*.18,2),"transport":"Nearby restaurant or food district."},
                {"time":"15:00","title":"Neighbourhood walk and local experience","description":"Explore nearby markets, viewpoints, museums, or cultural areas at a comfortable pace.","category":"Experience","estimated_cost":round(per_day*.18,2),"transport":"Walking where practical; otherwise local transit."},
                {"time":"19:00","title":"Dinner and evening leisure","description":"Choose a dining spot and leave flexibility for rest or an optional evening activity.","category":"Food","estimated_cost":round(per_day*.20,2),"transport":"Pre-book a safe return ride if needed."}
            ]
        })
    return {"summary":f"A {req.travel_style.lower()} {len(dates)}-day plan for {req.destination}, designed for {req.group_size} traveller(s). Demo suggestions are a starting point; verify details locally.",
            "days":days, "estimated_total":round(req.budget*.88,2),
            "tips":["Confirm opening hours, ticket prices, and local transport before departure.","Keep a contingency amount for unexpected expenses.","Use official tourism and transport sources for current information."]}

async def generate_content(req: TripRequest, dates: list[date]) -> tuple[dict, bool]:
    if not settings.groq_api_key:
        return demo_plan(req, dates), False
    payload = {
        "destination":req.destination, "dates":[d.isoformat() for d in dates],
        "budget":req.budget, "currency":req.currency, "style":req.travel_style,
        "interests":req.interests, "group_size":req.group_size, "pace":req.pace,
        "accommodation":req.accommodation, "notes":req.notes
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {settings.groq_api_key}"},
            json={"model":settings.groq_model,"temperature":0.6,
                  "messages":[{"role":"system","content":SYSTEM_PROMPT},
                              {"role":"user","content":json.dumps(payload)}]}
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"]
    raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(raw), True

def date_range(start: str, end: str) -> list[date]:
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    if b < a: raise ValueError("End date must be on or after start date.")
    if (b-a).days > 20: raise ValueError("Trips are limited to 21 days in this version.")
    return [a + timedelta(days=i) for i in range((b-a).days+1)]

def normalize(req: TripRequest, content: dict) -> dict:
    return {
        "id":str(uuid.uuid4()), "destination":req.destination,
        "start_date":req.start_date, "end_date":req.end_date,
        "budget":req.budget, "currency":req.currency,
        "travel_style":req.travel_style, "group_size":req.group_size,
        "summary":content.get("summary","Your personalized travel plan."),
        "days":content.get("days",[]),
        "estimated_total":float(content.get("estimated_total",0)),
        "tips":content.get("tips",[]), "ai_generated":bool(content.get("_ai",False)),
        "created_at":datetime.now(timezone.utc).isoformat()
    }
