from sqlite3 import connect
from datetime import datetime


class UserDatabase:
    
    def __init__(self, db_path: str, sql_path: str):
        self.sql_path = sql_path
        self.db_path = db_path
        
    def __enter__(self):
        self.db = connect(self.db_path)
        self.cur = self.db.cursor()
        
        with open(self.sql_path, encoding="UTF-8") as file:
            self.cur.executescript(file.read())
            
        return self
        
    def __exit__(self, exc_type, exc_val, traceback):
        
        if exc_val:
            print(f"Произошла ошибка: {exc_val}")
            
        try:
            self.db.commit()
        except Exception as e:
            print("При попытке сохранить данные произошла ошибка:\n", e, "\nДанные не сохранены")
            
        try:
            self.db.close()
        except Exception as e:
            print("При попытке закрыть соединение данные произошла ошибка:\n", e)
        
        return True
    
    def add_user(self, user):
        self.cur.execute("INSERT INTO users (id, reg_time, attempt_counter) VALUES (?, ?, ?)", 
                         (user.id, datetime.now().isoformat(), 0))
        
    def __contains__(self, user):
        self.cur.execute("SELECT 1 FROM users WHERE id = ?", (user.id,))
        return self.cur.fetchone() is not None
    
    def inc_att(self, user):
        self.cur.execute("UPDATE users SET attempt_counter=attempt_counter + 1 WHERE id=?", (user.id,))
        
    def get_att(self, user):
        return self.cur.execute("SELECT attempt_counter FROM users WHERE id=?", (user.id,)).fetchone()[0]


def check_db(user, db_path, sql_path):
    with UserDatabase(db_path=db_path, sql_path=sql_path) as db:
        if user not in db:
            db.add_user(user)
