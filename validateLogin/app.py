import bcrypt
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from jwtService import check_jwt_validity

uri = "mongodb+srv://admin:admin@lukacluster.cf5yzeq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sincekDB"]
collection = db["admin"]

def lambda_handler(event, context):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": "Database connection error"})}

    try:
        #parse
        request_body = json.loads(event.get('body'))
        entered_token = request_body.get('token')

        if not entered_token:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing token"})}
        
        item = collection.find_one({"token": entered_token})
        print(item)

        if item:
            token = item.get('token')


            if token == entered_token and check_jwt_validity(token):
                return {"statusCode": 200, "body": json.dumps({"valid": True})}
            else:
                return {"statusCode": 401, "body": json.dumps({"valid": False})}
        else:
            return {"statusCode": 404, "body": json.dumps({"error": "User not found, authentication failed"})}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
    
print(lambda_handler({"body": "{\"token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MDQ4MjAzODd9.W_ED3fpE_xCGwJOpdFU71-HmzNH8c1uIz-cXX3O9PFU\"}"}, None))
    