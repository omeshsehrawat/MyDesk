from supabase_client import supabase
import datetime


class Accessing_Table_Data:

    def __init__(self):
        self.today = datetime.date.today()
        self.today_start = f"{self.today}T00:00:00"
        self.today_end = f"{self.today}T23:59:59"

    # -------- TODAY DATA -------- #
    def access_today_data(self, table_name, user_id):
        data_column = "date"
        if table_name == "todo":
            date_column = "date"
        elif table_name == "expense":
            data_column = "expenditureDate"
        else:
            return []

        resp = supabase.table(table_name)\
            .select("*")\
            .eq("user_id", user_id)\
            .gte("date", self.today_start)\
            .lte("date", self.today_end)\
            .order("sr_no", desc=False)\
            .execute()

        rows = resp.data or []

        if table_name == "todo":
            return [[
                r["sr_no"], r["task"], r["date"],
                r["deadline"], r["status"]
            ] for r in rows]

        elif table_name == "expense":
            return [[
                r["sr_no"], r["item"], r["amount"],
                r["expenditureDate"], r["date"]
            ] for r in rows]

        return []

    # -------- RANGE DATA -------- #
    def access_data(self, table_name, first_date, last_date, user_id):
        start = f"{first_date}T00:00:00"
        end = f"{last_date}T23:59:59"

        resp = supabase.table(table_name)\
            .select("*")\
            .eq("user_id", user_id)\
            .gte("date", start)\
            .lte("date", end)\
            .order("sr_no", desc=False)\
            .execute()

        rows = resp.data or []

        if table_name == "todo":
            return [[
                r["sr_no"], r["task"], r["date"],
                r["deadline"], r["status"]
            ] for r in rows]

        elif table_name == "expense":
            return [[
                r["sr_no"], r["item"], r["amount"],
                r["expenditureDate"], r["date"]
            ] for r in rows]

        return []
