import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from requests_toolbelt.multipart import decoder
import base64
from jwtService import check_jwt_validity
from create import insert_image_into_mongodb
from delete import delete_from_mongodb
from get import get_all_images

uri = "mongodb+srv://admin:admin@lukacluster.cf5yzeq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sincekDB"]
admin_collection = db["admin"]

def lambda_handler(event, context):
    http_method = event.get('httpMethod')

    if http_method == 'DELETE':
        return handle_delete_request(event)
    elif http_method == 'POST':
        return handle_post_request(event)
    elif http_method == 'GET':
        return handle_get_request(event)
    else:
        return {"statusCode": 405, "body": json.dumps({"error": "Method not allowed"})}

def handle_delete_request(event):
    query_params = event.get('queryStringParameters', {})
    id, entered_token = query_params.get("id"), query_params.get("token")

    print(id, entered_token)

    if not (id and entered_token):
        return {"statusCode": 400, "body": json.dumps({"error": "Missing token or id"})}

    if is_valid_token(entered_token):
        data = delete_from_mongodb(id)
        return data
    else:
        return {"statusCode": 401, "body": json.dumps({"valid": False})}

def handle_post_request(event):
    print("Headers:", event['headers'])
    print("Content-Type:", event['headers']['content-type'])

    if event.get('isBase64Encoded', False):
        body = base64.b64decode(event['body'])
        print("isBase64Encoded")
    else:
        body = event['body']
        print("not isBase64Encoded")

    content_type_header = event['headers']['content-type']
    multipart_data = decoder.MultipartDecoder(body, content_type_header)

    entered_token = None
    image = None
    image_name = None
    description = None
    price = None

    for part in multipart_data.parts:
        # Each part will have a .headers and .content
        content_disposition = part.headers[b'Content-Disposition'].decode()
        part_name = None
        if 'name=' in content_disposition:
            part_name = content_disposition.split('name=')[1].strip('"')
            print("part name here: " + part_name)

        if part_name == 'token':
            entered_token = part.content.decode()
            print(entered_token)
        elif "image" in part_name:
            image = part.content  
        elif part_name == 'name':
            image_name = part.content.decode()
            print(image_name)
        elif part_name == 'description':
            description = part.content.decode()
            print(description)
        elif part_name == 'price':
            price = part.content.decode()
            print(price)

    if not entered_token:
        return {
                        'statusCode': 400,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'Missing token'}),
                        'isBase64Encoded': False    
        }
    
    if not is_valid_token(entered_token):
        return {
                        'statusCode': 403,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'Invalid token'}),
                        'isBase64Encoded': False
        }
    data = insert_image_into_mongodb(image, image_name, description, price)

    return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(data),
                'isBase64Encoded': False
                }



def handle_get_request(event):
        images = get_all_images()
        if images:
          return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(images)
        }
        else:
            return {"statusCode": 404, "body": json.dumps({"error": "No images found"})}

def is_valid_token(token):
    item = admin_collection.find_one({"token": token})
    if item and check_jwt_validity(item.get('token')):
        return True
    return False


#print(lambda_handler({"httpMethod": "GET"}, None))
"""for i in range(20):
    print(lambda_handler({"httpMethod": "POST", "body": json.dumps({"image_path": "bee.webp", "name": "test", "description": "test", "price": 1}), "queryStringParameters": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MDQ4MzUxNDN9.SQ2RlicKofEJUgpkxGJkdgaX3gWMg0m_JvLvxyolHAc"}}, None))
"""
#print(lambda_handler({"httpMethod": "DELETE", "body": json.dumps({"image_path": "bee.webp", "name": "test", "description": "test", "price": 1}), "queryStringParameters": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MDQ4MzUxNDN9.SQ2RlicKofEJUgpkxGJkdgaX3gWMg0m_JvLvxyolHAc", "id": "659d9e158c2af8f584e23c63"}}, None))
