from supabase_client import supabase
from datetime import datetime

def add_task(task, deadline, user_id, status="pending"):
    entry_date = datetime.utcnow().isoformat()
    supabase.table("todo").insert({
        "task": task,
        "status": status,
        "date": entry_date,
        "deadline": deadline,
        "user_id": user_id
    }).execute()

def get_tasks_by_user(user_id):
    resp = supabase.table("todo").select("*").eq("user_id", user_id).order("sr_no", desc=False).execute()
    return resp.data or []

def delete_tasks(sr_no, user_id):
    supabase.table("todo").delete().eq("sr_no", sr_no).eq("user_id", user_id).execute()

def update_task_status(sr_no, status, user_id):
    supabase.table("todo").update({"status": status}).eq("sr_no", sr_no).eq("user_id", user_id).execute()