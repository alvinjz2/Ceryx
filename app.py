from flask import Flask, request, redirect, abort

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def valid_request(request):
    accepted_brokers = ['IB'] 
    accepted_orders = []
    accepted_order_types = []
    valid_parameters = ['api_key', 'broker', 'timestamp', 'order', 'order_type', 'instrument', 'quantity', 'spot']
    error_code = ''
    if request[valid_parameters[0]] != 'alvinjz2':
        return (False, '0')
    if request[valid_parameters[1]] not in accepted_brokers:
        error_code += '1'
    if int(request[valid_parameters[6]]) <= 0:
        error_code += '6'
    return (False, error_code) if error_code != '' else (True, error_code)

@app.route('/not_authorized')
def deny():
    return 'Not authorized.'

@app.route("/buy", methods=['GET','POST'])
def execute_buy():
    if request.method == 'GET':
        token = request.args.get('api_key')
        if token == None:
            return "No API Key"
        elif token != 'alvinjz2':
            return redirect('/not_authorized')
        return "Success"
    else:
        return "Default"


@app.route("/sell", methods=['GET','POST'])
def execute_sell():
    if request.method == 'GET':
        token = request.args.get('api_key')
        if token == None:
            return "No API Key"
        elif token != 'alvinjz2':
            return redirect('/not_authorized')
        return "Success"
    else:
        return "Default"

@app.route('/json-example', methods=['GET','POST'])
def json_example():
    return 'JSON Object Example'
