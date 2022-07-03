from flask import Flask, request, redirect, abort
from flask import render_template

app = Flask(__name__)
app.config.from_object('config')


@app.route("/buy", methods=['POST'])
def execute_buy():
    return None


@app.route("/sell", methods=['POST'])
def execute_sell():
    return None


@app.route("/openorders", methods=['GET'])
def get_openorders():
    return None


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(threaded=True)