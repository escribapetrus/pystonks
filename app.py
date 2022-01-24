from flask import Flask, url_for, redirect
from markupsafe import escape
from stocks import rank 
from http_client import make_request
import os
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return redirect(url_for("my_stocks"))

@app.route("/my-stocks")
def my_stocks():
    url = os.environ["STOCK_INFO_SOURCE_URL"]
    stock_list = make_request(url)
    return json.dumps(rank(stock_list))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)