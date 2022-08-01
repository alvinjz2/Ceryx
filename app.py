from aioflask import Flask, request, Response, abort
import datetime
from db import Database, UserDetail


app = Flask(__name__)
app.config.from_object('config')

# Error Handling Section
token_expired = "Token is no longer valid since it has expired"
not_allowed = "Not authorized to perform this action"

@app.errorhandler(401)
def unauthorized(error):
    return not_allowed, 401

@app.errorhandler(403)
def forbidden(error):
    return not_allowed, 403

@app.errorhandler(410)
def gone(error):
    return token_expired, 410



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
    resp = await UserInfo(username, password)
    if time_expired(resp[UserDetail.expired.value]):
        abort(410)
    return resp[UserDetail.token.value]

@app.route("/register", methods=['POST'])
async def Register():
    token = request.args.get('token')
    if await UserInfo(token=token):
        new_user, new_pw, exp_time = request.args.get('new_user'), request.args.get('new_pw'), request.args.get('exp_time')
        Quant = Database('Quant')
        if new_user == None or new_pw == None:
            if exp_time == None:
                raise Exception 
            resp = Quant.add_user(None, None, exp_time)
        else:
            resp = Quant.add_user(new_user, new_pw, exp_time)
    return resp


async def UserInfo(username=None, password=None, token=None):
    Quant = Database('Quant')
    if username != None and password != None:
        resp = Quant.get_userinfo_via_userpass(username, password)
    elif token != None:
        resp = Quant.get_userinfo_via_token(token)
    else:
        # Unsupported auth method
        return Exception
    if resp is None:
        abort(401)
    return resp
    
async def AllowedWrite(token):
    resp = await UserInfo(token=token)
    if not resp:
        return False
    if time_expired(resp[UserDetail.expired.value]):
        abort(410)
    if resp[UserDetail.read.value]:
        return True

async def AllowedRead(token):
    resp = await UserInfo(token=token)
    if not resp:
        return False
    if time_expired(resp[UserDetail.expired.value]):
        abort(410)
    if resp[UserDetail.read.value]:
        return True
    else:
        abort(403)

def time_expired(expire_date):
    return True if datetime.datetime.now() > datetime.datetime.strptime(expire_date, '%m/%d/%Y') else False




if __name__ == '__main__':
    app.run(threaded=True)