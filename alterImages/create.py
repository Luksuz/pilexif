from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import bson

uri = "mongodb+srv://admin:admin@lukacluster.cf5yzeq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sincekDB"]
admin_collection = db["admin"]
images_collection = db["plantsInfo"]


def insert_image_into_mongodb(image, name, description, price):

    try:
        encoded_image = bson.binary.Binary(image)

        image_document = {
            "image": encoded_image,
            "name": name,
            "description": description,
            "price": price,
        }

        response = images_collection.insert_one(image_document)
        return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'created': str(response.inserted_id)}),
                'isBase64Encoded': False
            }
    except Exception as e:
         return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'massage': str(e)}),
                'isBase64Encoded': False
            }

