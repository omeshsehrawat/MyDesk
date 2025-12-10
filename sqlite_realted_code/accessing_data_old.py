import sqlite3
import datetime

class Accessing_Table_Data:

    def __init__(self):
        self.today_date = datetime.date.today()

    def access_today_data(self, table_name, user_id=None):
        db = sqlite3.connect("daily_use_database.db")  
        db.row_factory = sqlite3.Row
        cursor = db.cursor()      
        
        if user_id:
            cursor.execute(f"SELECT * FROM {table_name} WHERE date(date) = ? AND user_id=?",(str(self.today_date), user_id))

        else:
            cursor.execute(f"SELECT * FROM {table_name} WHERE date(date) = ?", (str(self.today_date),))

        rows = cursor.fetchall()
        data_list = [dict(row) for row in rows]

        for r in data_list:
            r.pop("user_id", None)

        # Convert dicts into lists in correct order for JS
        if table_name == "todo":
            data_list = [[r["sr_no"], r["task"], r["date"], r["deadline"], r["status"]] for r in data_list]
        elif table_name == "expense":
            data_list = [[r["sr_no"], r["item"], r["amount"], r["expenditureDate"], r["date"]] for r in data_list]
        
        cursor.close()
        db.close()

        return data_list
    
    def access_data(self, table_name, first_date, last_date=None, user_id=None):
        db = sqlite3.connect("daily_use_database.db")  
        db.row_factory = sqlite3.Row
        cursor = db.cursor() 
        if last_date is None:
            last_date = self.today_date

        if user_id:
            cursor.execute(f"SELECT * FROM {table_name} WHERE date(date) BETWEEN ? AND ? AND user_id=?",((str(first_date)), (str(last_date)), user_id))
        else:
            cursor.execute(f"SELECT * FROM {table_name} WHERE date(date) BETWEEN ? AND ?",((str(first_date)), (str(last_date))))
        
        rows = cursor.fetchall()
        data_list = [dict(row) for row in rows]

        for r in data_list:
            r.pop("user_id", None)

        # print(data_list)
        # Convert dicts into lists in correct order
        if table_name == "todo":
            data_list = [[r["sr_no"], r["task"], r["date"], r["deadline"], r["status"]] for r in data_list]
        elif table_name == "expense":
            data_list = [[r["sr_no"], r["item"], r["amount"], r["expenditureDate"], r["date"]] for r in data_list]
        # print(data_list)
        cursor.close()
        db.close()

        return data_list
   
