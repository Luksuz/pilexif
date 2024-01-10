from pymongo import MongoClient
from pymongo.server_api import ServerApi
import base64
from bson import ObjectId

uri = "mongodb+srv://admin:admin@lukacluster.cf5yzeq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sincekDB"]
images_collection = db["plantsInfo"]


def get_all_images():
    try:
        images = []
        for document in images_collection.find():
            #use bson to convert the objectid to a string
            image_id = str(document['_id'])
            image_binary = document['image']
            image_name = document['name']
            image_description = document['description']
            image_price = document['price']
        
            image_base64 = base64.b64encode(image_binary).decode('utf-8')   

            image_object = {
                "id" : image_id,
                "image": image_base64,
                "name": image_name,
                "description": image_description,
                "price": image_price
            }
            images.append(image_object)

        return images
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


