import bcrypt
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from jwtService import update_admin_jwt_token


def lambda_handler(event, context):
    uri = "mongodb+srv://admin:admin@lukacluster.cf5yzeq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["sincekDB"]
    collection = db["admin"]

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": "Database connection error"})}

    try:
        #parse
        request_body = json.loads(event.get('body'))
        entered_username = request_body.get('username')
        entered_password = request_body.get('password')

        if not entered_username or not entered_password:
            return {"statusCode": 400, "body": json.dumps({"error": "Username and password are required"})}

        item = collection.find_one({"username": entered_username})

        if item:
            stored_hashed_password = item.get('password')

            if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password):
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'token': update_admin_jwt_token(entered_username, collection)}),
                    'isBase64Encoded': False
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'message': 'Invalid credentials'}),
                    'isBase64Encoded': False
                }
        else:
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Invalid credentials'}),
                'isBase64Encoded': False
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'An error occurred'}),
            'isBase64Encoded': False
        }

print(lambda_handler({"body": "{\"username\": \"admin\", \"password\": \"s1nc3k!\"}"}, None))