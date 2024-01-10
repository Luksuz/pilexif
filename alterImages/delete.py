from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import ObjectId

uri = "mongodb+srv://admin:admin@lukacluster.cf5yzeq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sincekDB"]
images_collection = db["plantsInfo"]

def delete_from_mongodb(id):
    try:
        print(id)
        response = images_collection.delete_one({'_id': ObjectId(id)})
        print(response.deleted_count)

        # Check if a document was deleted
        if response.deleted_count > 0:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'success': True}),
                'isBase64Encoded': False
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'success': False, 'message': 'Document not found'}),
                'isBase64Encoded': False
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'success': False, 'error': str(e)}),
            'isBase64Encoded': False
        }


# Example usage
# delete_from_mongodb(your_id_here)
