from .config import settings

_memory: dict[str, dict] = {}
_client = None

def supabase_client():
    global _client
    if not settings.supabase_url or not settings.supabase_service_role_key:
        return None
    if _client is None:
        from supabase import create_client
        _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _client

def list_trips():
    client = supabase_client()
    if client:
        return client.table("itineraries").select("data").order("created_at", desc=True).execute().data
    return list(_memory.values())

def get_trip(trip_id: str):
    client = supabase_client()
    if client:
        rows = client.table("itineraries").select("data").eq("id", trip_id).limit(1).execute().data
        return rows[0]["data"] if rows else None
    return _memory.get(trip_id)

def save_trip(trip: dict):
    client = supabase_client()
    if client:
        client.table("itineraries").upsert({"id":trip["id"],"destination":trip["destination"],"created_at":trip["created_at"],"data":trip}).execute()
    else:
        _memory[trip["id"]] = trip
    return trip

def delete_trip(trip_id: str):
    client = supabase_client()
    if client:
        client.table("itineraries").delete().eq("id",trip_id).execute()
        return
    _memory.pop(trip_id, None)
