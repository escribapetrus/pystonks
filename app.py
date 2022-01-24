from flask import Flask, url_for, redirect, jsonify, request, make_response
from stocks import rank 
from http_client import make_request
from file_client import get_contents
from functools import wraps
import datetime
import os
import json
import jwt

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET"]

def authenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return json.dumps({"message": "a valid token is missing"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            current_user = data
        except:
            return json.dumps({"message": "token is invalid"})
        return f(current_user, *args, **kwargs)
    return decorator

@app.route("/")
def hello_world():
    return redirect(url_for("my_stocks"))

@app.route("/my-stocks")
def my_stocks():
    url = os.environ["STOCK_INFO_SOURCE_URL"]
    stock_list = make_request(url)
    return json.dumps(rank(stock_list))

@authenticated
@app.route("/restricted", methods=["GET"])
def restricted():
    return jsonify({"message": "restricted access granted"})

@app.route("/login", methods=["POST"])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify -- no auth", 401, {"Authentication": "Login required"})

    user = auth.username
    if user:
        token = jwt.encode({'public_id': user, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({"token": token})
     
    return make_response('could not verify -- no user',  401, {'Authentication': '"login required"'})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)