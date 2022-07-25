import sqlite3
"""
table scheme:
token user pass admin read write

token: access token to call API endpoints
expire time: when it becomes expired
user: username, hashed
pass: password, hashed
admin: can generate new user sign up keys, can modify other read write permissions
read: only get requests
write: only post requests

token to api request because what if temp user, might not need to store info in db

"""


class Database:
    def __init__(self, db_name) -> None:
        self.db = None
        try:
            self.db = sqlite3.connect(f'{db_name}.db')
            self.c = self.db.cursor()
        except:
            raise Exception
        self.c.execute("""Create Table If Not Exists Users 
        (token text default null, expire_time text default null, 
        username text default null, password text default null, 
        admin integer default 0, read integer default 1, write integer default 0) """)

        self.c.execute("""Create Table If Not Exists Log 
        (timestamp text default null, token text default null, method text default null) """)

    def add_action(self):
        params = ('Log')

    def add_user(self, token, username="", password="", expire = "", admin = "", read = 1, write = 0):
        params = ('Users', ('token', 'expire', 'username', 'password', 'admin', 'read', 'write'), (token, expire, username, password, admin, read, write))
        return self.insert_row(params)

    def insert_row(self, params):
        # Table, Columns, Data
        try:
            self.c.execute("""Insert into ? ? Values ? """, params)
            return True
        except:
            return False
        
    def get_userinfo(self, username, password, token=""):
        params = ('Users', username, password, token)
        return self.select_row(params)

    def select_row(self, params):
        resp = self.c.execute("""Select * from ? Where (username=? AND password=?) OR token = ?""", params)
        return resp

    def __del__(self) -> None:
        try:
            self.c.close()
        except:
            print(f'Could not close connection')
            raise Exception
