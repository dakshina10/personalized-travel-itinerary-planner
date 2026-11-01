from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from .config import settings
from .models import TripRequest, UpdateTripRequest
from .services import date_range, generate_content, normalize
from . import storage

app = FastAPI(title="Personalized Travel Itinerary Planner API", version="1.0.0",
              description="Generate, save, edit, and manage personalized travel itineraries.")
app.add_middleware(CORSMiddleware, allow_origins=settings.origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status":"ok","service":"travel-planner-api"}

@app.post("/api/itineraries/generate")
async def generate(req: TripRequest):
    try:
        dates = date_range(req.start_date, req.end_date)
        content, is_ai = await generate_content(req, dates)
        content["_ai"] = is_ai
        trip = normalize(req, content)
        storage.save_trip(trip)
        return trip
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not generate itinerary: {str(exc)}")

@app.get("/api/itineraries")
def list_itineraries():
    rows = storage.list_trips()
    return [r.get("data", r) for r in rows]

@app.get("/api/itineraries/{trip_id}")
def get_itinerary(trip_id: str):
    trip = storage.get_trip(trip_id)
    if not trip: raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@app.put("/api/itineraries/{trip_id}")
def update_itinerary(trip_id: str, payload: UpdateTripRequest):
    if trip_id != payload.itinerary.id:
        raise HTTPException(status_code=400, detail="Trip ID mismatch")
    if not storage.get_trip(trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    storage.save_trip(payload.itinerary.model_dump())
    return payload.itinerary

@app.post("/api/itineraries/{trip_id}/regenerate")
async def regenerate_itinerary(trip_id: str):
    old = storage.get_trip(trip_id)
    if not old: raise HTTPException(status_code=404, detail="Trip not found")
    req = TripRequest(destination=old["destination"],start_date=old["start_date"],end_date=old["end_date"],
        budget=old["budget"],currency=old["currency"],travel_style=old["travel_style"],
        group_size=old["group_size"])
    try:
        dates = date_range(req.start_date, req.end_date)
        content, is_ai = await generate_content(req, dates)
        content["_ai"] = is_ai
        trip = normalize(req, content)
        storage.delete_trip(trip_id)
        storage.save_trip(trip)
        return trip
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not regenerate itinerary: {str(exc)}")

@app.delete("/api/itineraries/{trip_id}")
def delete_itinerary(trip_id: str):
    if not storage.get_trip(trip_id): raise HTTPException(status_code=404, detail="Trip not found")
    storage.delete_trip(trip_id)
    return {"message":"Trip deleted"}

@app.get("/api/destination-image")
async def destination_image(query: str = Query(min_length=2, max_length=100)):
    if not settings.unsplash_access_key:
        return {"url":None}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get("https://api.unsplash.com/search/photos",
            params={"query":query,"per_page":1,"orientation":"landscape"},
            headers={"Authorization":f"Client-ID {settings.unsplash_access_key}"})
        response.raise_for_status()
        results = response.json().get("results",[])
        return {"url":results[0]["urls"]["regular"] if results else None}
