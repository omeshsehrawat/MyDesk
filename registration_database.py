from supabase_client import supabase
from werkzeug.security import generate_password_hash
from typing import Optional
from postgrest.exceptions import APIError

def add_user(email, username, password):
    try:
        supabase.table("users").insert({
            "email": email,
            "username": username,
            "password": password
        }).execute()

        return True
    
    except APIError as e:
        # print("Supabase APIerror:", e)
        return False

    except Exception as e:
        # print("Unknown error:", e)
        return False
        
    
def get_user_by_email(email):
    resp = supabase.table("users").select("*").eq("email", email).limit(1).execute()

    # print("SUPABASE RESPONSE", resp.data)
    
    if resp.data and len(resp.data) > 0:
        return resp.data[0]
    return None

def get_all_users():
    resp = supabase.table("users").select("id, email, username, password").execute()
    return resp.data or []