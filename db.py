import sqlite3

class Database:
    def __init__(self, db_name) -> None:
        self.db = None
        try:
            self.db = sqlite3.connect(f'{db_name}.db')
            self.c = self.db.cursor()
        except:
            print(f'Could not connect to database')
            raise Exception
        self.c.execute("""Create Table If Not Exists ? (username text, password text, permissions text) """, (db_name))

    def is_user(self, username, password) -> None:
        t = self.c.execute("""Select Token from Permissions Where username=? and password=?""", (username, password))
        for row in t:
            print(row)
        return None

    def get_token(self, username, password) -> None:
        raise NotImplemented
    def insert(self) -> None:
        t = self.c.execute("""Insert into Permissions (username, password, permissions) Values ('quant', 'quant', 'all')""")

    def delete(self) -> None:
        return None
        
    def __del__(self) -> None:
        try:
            self.c.close()
        except:
            print(f'Could not close connection')
            raise Exception
