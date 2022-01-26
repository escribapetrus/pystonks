from flask import Flask, jsonify, url_for, redirect
from stocks import rank, simplify
from http_client import make_request
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return redirect(url_for("my_stocks"))

@app.route("/my-stocks")
def my_stocks():
    url = os.environ["STOCK_INFO_SOURCE_URL"]
    stock_list = make_request(url)
    return jsonify(rank(stock_list))

@app.route("/my-stocks/simple")
def my_stocks_simple():
    url = os.environ["STOCK_INFO_SOURCE_URL"]
    stock_list = make_request(url)
    return jsonify(simplify(rank(stock_list)))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)