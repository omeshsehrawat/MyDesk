from supabase_client import supabase
from datetime import datetime

def add_expense(item, amount, date, user_id):
    entry_date = datetime.utcnow().isoformat()
    supabase.table("expense").insert({
        "item": item,
        "amount": amount,
        "expenditureDate": date,
        "date": entry_date,
        "user_id": user_id
    }).execute()

def delete_expense(sr_no, user_id):
    supabase.table("expense").delete().eq("sr_no", sr_no).eq("user_id", user_id).execute()