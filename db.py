import sqlite3

class database:
    def __init__(self, db_name) -> None:
        self.db = None
        try:
            self.db = sqlite3.connect(db_name)
            self.c = self.db.cursor()
        except:
            print(f'Could not connect to database')
            raise Exception

    def select(self) -> None:
        return None

    def delete(self) -> None:
        return None
        
    def __del__(self) -> None:
        try:
            self.c.close()
        except:
            print(f'Could not close connection')
            raise Exception