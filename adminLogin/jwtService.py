import jwt
from datetime import datetime, timedelta



def generate_jwt_token(user_id):
    # Set the token expiration time (e.g., 1 day)
    expiration_time = datetime.now() + timedelta(hours=1)

    # Create a payload for the JWT containing user information
    payload = {
        "user_id": user_id,
        "exp": expiration_time,
    }

    # Generate the JWT token
    secret_key = "s!nc3k1"  # Replace with your own secret key for signing
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token



def update_admin_jwt_token(entered_username, collection):
    filter = {"username": entered_username}
    token = generate_jwt_token(1)

    update = {
        "$set": {
            "token": token,
            "token_timestamp": datetime.now().isoformat()
        }
    }

    result = collection.update_one(filter, update)
    if result.modified_count > 0:
        return token
    else:
        return { "error": "Token update failed" }
