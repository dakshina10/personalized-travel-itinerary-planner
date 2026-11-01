-- Run this in the Supabase SQL Editor.
-- Authenticated users own their trips. Backend service-role access bypasses RLS;
-- if you later expose direct client CRUD, use the user_id policies below.

create table if not exists public.itineraries (
  id uuid primary key,
  user_id uuid references auth.users(id) on delete cascade,
  destination text not null,
  created_at timestamptz not null default now(),
  data jsonb not null
);

alter table public.itineraries enable row level security;

drop policy if exists "Users can view their own itineraries" on public.itineraries;
create policy "Users can view their own itineraries"
on public.itineraries for select to authenticated
using (auth.uid() = user_id);

drop policy if exists "Users can insert their own itineraries" on public.itineraries;
create policy "Users can insert their own itineraries"
on public.itineraries for insert to authenticated
with check (auth.uid() = user_id);

drop policy if exists "Users can update their own itineraries" on public.itineraries;
create policy "Users can update their own itineraries"
on public.itineraries for update to authenticated
using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "Users can delete their own itineraries" on public.itineraries;
create policy "Users can delete their own itineraries"
on public.itineraries for delete to authenticated
using (auth.uid() = user_id);

create index if not exists itineraries_created_at_idx on public.itineraries (created_at desc);
