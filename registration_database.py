from supabase_client import supabase
from werkzeug.security import generate_password_hash
from typing import Optional

def add_user(email, username, password):
    # hashed = generate_password_hash(password)
    hashed = password
    try:
        resp = supabase.table("users").insert({
            "email":email,
            "username": username,
            "password":hashed
        }).execute()

        if resp.status_code in (200, 201) and resp.data:
            return True
        return False
    
    except Exception as e:
        return False
    
def get_user_by_email(email):
    resp = supabase.table("users").select("*").eq("email", email).limit(1).execute()

    print("SUPABASE RESPONSE", resp.data)
    
    if resp.data and len(resp.data) > 0:
        return resp.data[0]
    return None

def get_all_users():
    resp = supabase.table("users").select("id, email, username, password").execute()
    return resp.data or []