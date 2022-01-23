from flask import Flask
from flask import url_for
from markupsafe import escape
from stocks import rank 
from http_client import make_request
import os
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World</h1>"

@app.route("/my-stocks")
def my_stocks():
    url = os.environ["STOCK_INFO_SOURCE_URL"]
    stock_list = make_request(url)
    return json.dumps(rank(stock_list))

@app.route("/<name>")
def hello(name):
    return f"<h1>Hello, {escape(name)}</h1>"

@app.route("/myjson")
def my_json():
    x = {
        "a": "alpha",
        "b": "beta",
        "letters": "abcdef"
    }
    return x
