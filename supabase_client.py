import os
from supabase import create_client, Client

# SUPABASE_URL = os.getenv("DATABASE_URL")
# SUPABASE_KEY = os.getenv("DATABASE_API_KEY")

SUPABASE_URL = "https://lfbwrnedifenstwdpdcr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxmYndybmVkaWZlbnN0d2RwZGNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQyMjcxMzQsImV4cCI6MjA3OTgwMzEzNH0.5VciWaE9yALIfwaH0Iy81KxyL_ZBB6kDgGON47puG3I"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY env vars")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)