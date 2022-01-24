import jwt
import json

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
            current_user = 1
        except:
            return json.dumps({"message": "token is invalid"})
        return f(current_user, *args, **kwargs)
    return decorator