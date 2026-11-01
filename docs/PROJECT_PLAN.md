# Project Plan — Personalized Travel Itinerary Planner

## Objective
Build an individual full-stack application that reduces travel-planning effort by converting user preferences into structured, editable day-wise itineraries.

## Scope
React/Vite client, FastAPI REST API, optional Supabase Auth and PostgreSQL persistence, Groq-hosted generative AI, and optional Unsplash destination imagery.

## 10 Epics and 24 Tasks

| Epic | Task IDs | Tasks |
|---|---|---|
| 1. Project foundation | T01–T02 | T01 Set up repository and frontend/backend structure; T02 Configure environment variables and development scripts |
| 2. User interface | T03–T05 | T03 Build responsive SaaS dashboard; T04 Build navigation and saved-trip overview; T05 Add mobile-friendly layouts and status feedback |
| 3. Trip input | T06–T08 | T06 Build destination and date form; T07 Capture budget, currency, group size and accommodation; T08 Capture travel style, pace, interests and notes |
| 4. Backend API | T09–T10 | T09 Create FastAPI app, validation and health endpoint; T10 Implement itinerary CRUD REST endpoints |
| 5. Generative AI | T11–T12 | T11 Integrate Groq chat-completions API; T12 Add demo fallback and structured JSON itinerary generation |
| 6. Itinerary experience | T13–T15 | T13 Render day-wise activities and timelines; T14 Add inline editing and save; T15 Add regeneration and deletion |
| 7. Data and authentication | T16–T18 | T16 Create Supabase database schema and RLS; T17 Add optional Supabase sign-in; T18 Add backend persistence adapter and local demo storage |
| 8. Recommendations and logistics | T19–T20 | T19 Include attractions, meals, stays and transport suggestions; T20 Calculate estimated trip spend and show planning tips |
| 9. Quality and safety | T21–T22 | T21 Add API error handling, validation and CORS; T22 Document estimation limits and safe secret handling |
| 10. Release readiness | T23–T24 | T23 Write setup, configuration and deployment instructions; T24 Prepare GitHub checklist, scenarios and architecture documentation |

## Acceptance criteria
- A user can enter destination, dates, budget, interests, style, pace and group size.
- A generated response contains multiple days with time, activity, description, category, cost and transport.
- A user can save, view, edit, regenerate and delete a trip.
- The project starts locally using documented commands.
- No secrets are committed.
- Demo mode works without third-party API credentials.

## Scenarios
1. Solo traveller plans a weekend getaway with sightseeing and food interests.
2. Couple creates a relaxed, scenic, premium-style vacation and edits activities.
3. Friends plan a multi-day trip using group size, combined interests and a shared budget input.

## Individual project responsibilities
The individual developer is responsible for requirements, UI, API, AI prompt design, database integration, testing, documentation, deployment and GitHub maintenance.
