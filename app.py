from aioflask import Flask, request, Response
from flask import render_template
import asyncio

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


async def Authenticate(token, method):
    # Check if token exists in the permissions table.
    # Client will have a call to see if the user exists (token associated with user)
    # but permissions for Ceryx are not defined. 
    raise NotImplemented




if __name__ == '__main__':
    app.run(threaded=True)