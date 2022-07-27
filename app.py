from cmath import exp
from aioflask import Flask, request, Response
import secrets
from datetime import datetime, strptime

from db import Database
import asyncio
import bcrypt
from enum import Enum, auto
app = Flask(__name__)
app.config.from_object('config')

@app.route("/buy", methods=['POST'])
async def execute_buy():
    token = request.args.get('token')
    if await AllowedWrite(token):
        return True



@app.route("/sell", methods=['POST'])
async def execute_sell():
    token = request.args.get('token')
    if await AllowedWrite(token):
        return True


@app.route("/openorders", methods=['GET'])
async def get_openorders():
    token = request.args.get('token')
    if await AllowedRead(token):
        return True


@app.route("/profitandloss", methods=['GET'])
async def get_profitandloss():
    token = request.args.get('token')
    if await AllowedRead(token):
        return True


@app.route("/authenticate", methods=['POST'])
async def Authenticate():
    # Check if token exists in the permissions table.
    # Client will have a call to see if the user exists (token associated with user)
    # but permissions for Ceryx are not defined. 
    # could have read/write permission sets, aka two tables for each
    username, password = request.args.get('user'), request.args.get('pw')
    params = [UserDetail.token, UserDetail.expired]
    resp = await UserInfo(username, password, params)
    if datetime.datetime.now() > strptime(resp[UserDetail.expired]):
        return False
    return resp[UserDetail.token]

@app.route("/register", methods=['POST'])
async def Register():
    token = request.args.get('token')
    if await UserInfo(token=token, params=[UserDetail.admin]):
        new_user, new_pw, exp_time = request.args.get('new_user'), request.args.get('new_pw'), request.args.get('exp_time')
        Quant = Database('Quant')
        secret_token = secrets.token_hex(16)
        if new_user == None or new_pw == None:
            if exp_time == None:
                raise Exception 
            resp = Quant.add_user(secret_token, expire=exp_time)
        else:
            resp = Quant.add_user(secret_token, username=new_user, password=new_pw, expire=exp_time)
    return resp


async def UserInfo(username="", password="", params=[], token=""):
    if not len(params):
        raise Exception
    Quant = Database('Quant')
    hash_pw = bcrypt.hashpw(password, bcrypt.gensalt(12))
    resp = Quant.get_userinfo(username, hash_pw, token)
    if resp is None:
        return False
    return [resp[p] for p in params] if len(params) > 1 else resp[params[0]]
    
async def AllowedWrite(token):
    resp = await UserInfo(token=token, params=[UserDetail.write, UserDetail.expired])
    if not resp:
        return False
    if datetime.datetime.now() > strptime(resp[UserDetail.expired]):
        return False
    if resp[UserDetail.read]:
        return True

async def AllowedRead(token):
    resp = await UserInfo(token=token, params=[UserDetail.read, UserDetail.expired])
    if not resp:
        return False
    if datetime.datetime.now() > strptime(resp[UserDetail.expired]):
        return False
    if resp[UserDetail.read]:
        return True

class UserDetail(Enum):
    token = 0
    expired = auto()
    user = auto()
    password = auto()
    admin = auto()
    read = auto()
    write = auto()


if __name__ == '__main__':
    app.run(threaded=True)