# Personalized Travel Itinerary Planner

A full-stack, AI-assisted travel planner built with **React + Vite**, **FastAPI**, and **Supabase**. It creates day-wise trip plans from a destination, dates, budget, travel style, interests, and group size. Users can save, view, edit, and regenerate plans.

> This repository is prepared for GitHub. Never commit real API keys, passwords, access tokens, or `.env` files.

## Features

- Responsive SaaS-style dashboard and trip builder
- AI itinerary generation through Groq (Llama model), with a deterministic demo fallback
- Day-wise schedule with attractions, meals, accommodation suggestions, transport notes, and estimated costs
- Budget summary and trip preference controls
- Save, view, edit, delete, and regenerate trips
- Optional Supabase authentication and PostgreSQL persistence
- Optional Unsplash image integration
- API validation, CORS configuration, health endpoint, and example environment files
- Three documented user scenarios: solo weekend, couple vacation, and group trip

## Architecture

```text
Browser (React + Vite)
       |
       | REST / JSON
       v
FastAPI backend
   |       |        |
   |       |        +---- Unsplash API (optional destination imagery)
   |       +------------- Groq API (optional AI generation)
   +--------------------- Supabase Auth + PostgreSQL (optional persistence)
```

The application can be run locally without external credentials using demo mode. For persistent accounts and data, configure Supabase. For AI-generated content, configure Groq.

## Repository structure

```text
.
├── frontend/                 # React + Vite application
├── backend/                  # FastAPI service
├── supabase/schema.sql       # Database schema and RLS policies
├── docs/                     # Project plan, architecture, task tracker
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- Node.js 18+
- npm
- Optional: Supabase project and Groq API key
- Optional: Unsplash access key

## 1. Run the backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env     # Windows
# cp .env.example .env     # macOS/Linux
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

## 2. Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
copy .env.example .env     # Windows
# cp .env.example .env     # macOS/Linux
npm run dev
```

Frontend: `http://localhost:5173`

## 3. Configure optional services

### Groq AI
Create an API key in the Groq developer console and set these values in `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

If no key is configured, the backend uses a clearly identified demo itinerary generator.

### Supabase
1. Create a Supabase project.
2. Run `supabase/schema.sql` in the Supabase SQL Editor.
3. Set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `backend/.env`.
4. Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in `frontend/.env`.
5. Enable Email authentication in Supabase Authentication settings.

The frontend uses Supabase Auth when configured. The backend uses Supabase for trip persistence when configured; otherwise, it uses in-memory demo storage (data resets when the backend restarts).

**Security:** Keep the Supabase service-role key on the backend only. Never put it in a `VITE_` variable or commit it.

### Unsplash (optional)
Set `UNSPLASH_ACCESS_KEY` in `backend/.env`. Without it, the app uses a neutral gradient image treatment.

## Environment variables

See `backend/.env.example` and `frontend/.env.example`. Do not replace placeholders with real secrets in files committed to GitHub.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/api/itineraries/generate` | Generate an itinerary |
| GET | `/api/itineraries` | List saved trips |
| GET | `/api/itineraries/{trip_id}` | Get one trip |
| PUT | `/api/itineraries/{trip_id}` | Update a trip |
| POST | `/api/itineraries/{trip_id}/regenerate` | Regenerate a trip |
| DELETE | `/api/itineraries/{trip_id}` | Delete a trip |
| GET | `/api/destination-image?query=...` | Optional destination image |

## GitHub upload checklist

1. Extract this project folder.
2. Open a terminal inside the project folder.
3. Run `git init`.
4. Run `git add .`.
5. Run `git commit -m "Initial commit: travel itinerary planner"`.
6. Create an empty GitHub repository.
7. Add its URL as the remote: `git remote add origin YOUR_GITHUB_REPOSITORY_URL`.
8. Run `git branch -M main` and `git push -u origin main`.
9. Add your deployed frontend demo URL and GitHub repository URL to your project submission page.

Before pushing, confirm that `.env` files and API keys are not staged.

## Deployment

- Frontend: Vercel or Netlify. Set `VITE_API_BASE_URL` to the deployed backend URL and configure Supabase public variables.
- Backend: Render, Railway, or another Python ASGI host. Set the environment variables in the host dashboard and use:
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Supabase: use the SQL schema and configure Auth redirect URLs for the deployed frontend.

Update CORS origins in `backend/.env` to include the deployed frontend domain.

## Important limitations

- AI suggestions can be inaccurate or outdated. Confirm opening hours, ticket prices, routes, visa rules, and bookings with official providers before travel.
- Travel time and costs are estimates, not live navigation or booking data.
- Group collaboration is represented by group size and shared planning inputs in this starter version; real-time multi-user editing/invitations can be added as a later enhancement.
- Demo mode stores trips in memory and is not suitable for production.

## Project scenarios

1. **Solo weekend getaway:** short dates, modest budget, sightseeing and food interests; generates a balanced plan.
2. **Couple vacation:** relaxed pacing, scenic activities, premium accommodation preference; supports editing and regeneration.
3. **Small group trip:** group size and combined interests influence activities, estimated costs, and transport suggestions.

## License

MIT. See `LICENSE`.
