from aioflask import Flask, request, Response
from db import Database
from flask import render_template
import asyncio
import bcrypt

app = Flask(__name__)
app.config.from_object('config')


@app.route("/buy", methods=['POST'])
async def execute_buy():
    allowed = await Authenticate(request.args.get('token'), 'buy')
    if not allowed: 
        return 
    raise NotImplemented


@app.route("/sell", methods=['POST'])
async def execute_sell():
    raise NotImplemented


@app.route("/openorders", methods=['GET'])
async def get_openorders():
    raise NotImplemented


@app.route("/profitandloss", methods=['GET'])
async def get_profitandloss():
    raise NotImplemented

@app.route("/authenticate", methods=['POST'])
async def Authenticate():
    # Check if token exists in the permissions table.
    # Client will have a call to see if the user exists (token associated with user)
    # but permissions for Ceryx are not defined. 
    # could have read/write permission sets, aka two tables for each
    username, password  = request.args.get('user'), request.args.get('pw')
    RegisteredUsers = Database("RegisteredUsers") # Go to registered users to retrieve token
    hash_user = bcrypt.hashpw(username, bcrypt.gensalt(4))
    hash_pw = bcrypt.hashpw(password, bcrypt.gensalt(12))
    try:
        return RegisteredUsers.get_token(hash_user, hash_pw)
    except:
        raise Exception

    raise NotImplemented




if __name__ == '__main__':
    app.run(threaded=True)