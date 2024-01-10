import jwt
from datetime import datetime

def check_jwt_validity(stored_token):
    decoded_token = jwt.decode(stored_token, "s!nc3k1", algorithms=["HS256"])
    token_exp = decoded_token["exp"]
    current_time = datetime.now()

    if token_exp >= current_time.timestamp():
        # Token is valid, user is authenticated
        return {"validated": True}
    else:
        return {"validated": False}
