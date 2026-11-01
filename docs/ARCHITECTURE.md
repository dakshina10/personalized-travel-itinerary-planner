# Technical Architecture

## Component responsibilities

- **React + Vite:** dashboard, trip builder, itinerary timeline, editing controls and Supabase client authentication.
- **FastAPI:** request validation, itinerary orchestration, REST endpoints, optional provider integrations and storage abstraction.
- **Groq AI:** transforms structured preferences into a JSON itinerary using a constrained prompt.
- **Supabase:** optional authentication and PostgreSQL persistence.
- **Unsplash:** optional destination imagery endpoint.

## Request lifecycle

1. User submits trip preferences from the React form.
2. Frontend sends JSON to `POST /api/itineraries/generate`.
3. FastAPI validates the dates and request fields.
4. Service selects Groq AI when configured; otherwise it generates a demo itinerary.
5. Backend normalizes the response into the application itinerary model.
6. Storage adapter saves the trip to Supabase or in-memory demo storage.
7. React renders the itinerary and refreshes the saved-trip dashboard.

## Data flow diagram

```text
Traveler
   |
   v
React Dashboard / Trip Builder
   |
   | HTTPS JSON
   v
FastAPI REST API
   |              |               |
   v              v               v
Groq AI       Supabase DB      Unsplash
   |              |
   +------ JSON itinerary ------+
                  |
                  v
        Itinerary timeline
        Edit / Save / Regenerate
```

## Security notes
- Keep service-role keys on the backend.
- Use environment variables and never commit `.env`.
- Restrict CORS to known frontend origins in deployment.
- The supplied schema enables RLS for authenticated direct database access.
- Before production, enforce user ownership in backend routes and pass verified Supabase JWT claims to the API. This starter's service-role persistence adapter is intended for a controlled demo, not a multi-tenant production launch.
