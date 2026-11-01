# Testing and Verification

## Manual smoke test

1. Start FastAPI and verify `GET /health` returns `{"status":"ok","service":"travel-planner-api"}`.
2. Start Vite and open the dashboard.
3. Create a trip with a valid destination, date range, budget and interests.
4. Confirm the itinerary contains day headings and scheduled activities.
5. Refresh the page and confirm the saved trip appears in the dashboard while the backend process remains running.
6. Open a trip, edit an activity title, save, and verify the updated title.
7. Regenerate a trip and verify a new itinerary is displayed.
8. Delete a trip and confirm it disappears from the dashboard.
9. Test invalid dates and a missing destination.
10. Configure Groq and verify the AI-generated indicator; remove the key and verify demo fallback.

## Known demo-mode behavior
- In-memory saved trips are cleared when the backend restarts.
- Sign-in requires configured Supabase public environment variables.
- Supabase backend persistence requires the backend URL and service-role key.
- AI and destination images require their respective provider keys.
