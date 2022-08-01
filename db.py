import datetime
import sqlite3
import bcrypt
import secrets
from enum import Enum, auto



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
class UserDetail(Enum):
    token = 0
    expired = auto()
    user = auto()
    password = auto()
    admin = auto()
    salt = auto()
    read = auto()
    write = auto()


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
        salt text default null, admin integer default 0, 
        read integer default 1, write integer default 0) """)

        self.c.execute("""Create Table If Not Exists Log 
        (timestamp text default null, token text default null, method text default null) """)

    def add_action(self, timestamp, token, action):
        self.c.execute("""Insert Into Log Values (?, ?, ?)""" , (timestamp, token, action))
        self.db.commit()

    def add_user(self, username=None, password=None, expire = None, admin = 0, read = 1, write = 0):
        secret_token = secrets.token_hex(16)
        salt = bcrypt.gensalt(12)
        hash_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        salt = salt.decode('utf-8')
        params = [secret_token, expire, username, hash_pw, salt, admin, read, write]
        try:
            self.c.execute("""Insert Into Users Values (?, ?, ?, ?, ?, ?, ?, ?)""", params)
            self.db.commit()
            return True
        except Exception as e:
            return e


    def get_userinfo_via_userpass(self, username, password):
        user_pass_query = self.c.execute("""Select * from Users Where username=? """, [username])
        user_pass_info = list(user_pass_query.fetchone())
        db_pw = user_pass_info[UserDetail.password.value]

        if bcrypt.checkpw(password.encode('utf-8'), db_pw.encode('utf-8')):
            return user_pass_info
        else:
            print('Incorrect Password')
            return False


    def get_userinfo_via_token(self, token):
        token_query = self.c.execute("""Select * from Users Where token = ?""", [token])
        token_info = list(token_query.fetchone())
        return token_info if token_info else False


    def user_exists(self, username=None, password=None, token=None):
        userpass = self.c.execute("""Select Exists (Select 1 from Users Where (username=? AND password=?) Limit 1) """, [username, password])
        token = self.c.execute("""Select Exists (Select 1 from Users Where token=? Limit 1)""", [token])
        return True if userpass.fetchone[0] or token.fetchone[0] else False


    def __del__(self) -> None:
        try:
            self.db.close()
        except:
            print(f'Could not close connection')
            raise Exception
