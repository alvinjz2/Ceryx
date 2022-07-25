from aioflask import Flask, request, Response
from requests import NullHandler
from db import Database
from flask import render_template
import asyncio
import bcrypt
from enum import Enum, auto
app = Flask(__name__)
app.config.from_object('config')

# write trade to db if successful
@app.route("/buy", methods=['POST'])
async def execute_buy():
    token = request.args.get('token')
    if UserInfo(token=token, params=[UserDetail.write]):
        return True
    raise NotImplemented


@app.route("/sell", methods=['POST'])
async def execute_sell():
    token = request.args.get('token')
    if UserInfo(token=token, params=[UserDetail.write]):
        return True
    raise NotImplemented


@app.route("/openorders", methods=['GET'])
async def get_openorders():
    token = request.args.get('token')
    if UserInfo(token=token, params=[UserDetail.read]):
        return True
    raise NotImplemented


@app.route("/profitandloss", methods=['GET'])
async def get_profitandloss():
    token = request.args.get('token')
    if UserInfo(token=token, params=[UserDetail.read]):
        return True
    raise NotImplemented

@app.route("/authenticate", methods=['POST'])
async def Authenticate():
    # Check if token exists in the permissions table.
    # Client will have a call to see if the user exists (token associated with user)
    # but permissions for Ceryx are not defined. 
    # could have read/write permission sets, aka two tables for each
    username, password = request.args.get('user'), request.args.get('pw')
    params = [UserDetail.token]
    resp = UserInfo(username, password, params)
    return resp

@app.route("/register", methods=['POST'])
async def Register():
    if request.args.get('')
    raise NotImplemented


async def UserInfo(username="", password="", params=[], token=""):
    if not len(params):
        raise Exception
    Quant = Database("Quant") # Go to registered users to retrieve token
    hash_pw = bcrypt.hashpw(password, bcrypt.gensalt(12))
    resp = Quant.get_userinfo(username, hash_pw, token)
    if resp is None:
        return False
    return [resp[p] for p in params] if len(params) > 1 else resp[params[0]]
    
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