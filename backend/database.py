"""
database.py - Supabase connection and table access
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_supabase: Client = None

def get_db() -> Client:
    global _supabase
    if _supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not found in environment!")
        try:
            _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("[OK] Connected to Supabase")
        except Exception as e:
            print(f"[ERROR] Supabase connection failed: {e}")
            raise
    return _supabase

# Table accessors
def users_collection():
    return get_db().table("users")

def tasks_collection():
    return get_db().table("tasks")

def moods_collection():
    return get_db().table("moods")
