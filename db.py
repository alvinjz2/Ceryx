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
            self.db = sqlite3.connect(f'Quant.db')
            self.c = self.db.cursor()
        except:
            raise Exception
        self.c.execute("""Create Table If Not Exists ? (username text, password text, permissions text) """, (db_name))

    def is_user(self, username, password) -> None:
        t = self.c.execute("""Select * from Permissions Where username=? and password=?""", (username, password))
        for row in t:
            print(row)
        return None

    def get_userinfo(self, username, password) -> None:
        raise NotImplemented

    def __del__(self) -> None:
        try:
            self.c.close()
        except:
            print(f'Could not close connection')
            raise Exception
