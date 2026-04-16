import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client
from database import users_collection
from datetime import datetime, timezone

user_doc = {
    "name":       "Test User",
    "email":      "test1@example.com",
    "password":   "testpass",
    "created_at": datetime.now(timezone.utc).isoformat(),
}

print("Attempting to insert...")
try:
    res = users_collection().insert(user_doc).execute()
    print("Success:", res.data)
except Exception as e:
    print("Exception:")
    import traceback
    traceback.print_exc()
