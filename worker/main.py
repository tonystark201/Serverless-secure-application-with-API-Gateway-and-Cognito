import uuid
import json
import logging


logger = logging.getLogger()


def lambda_handler(event, context):
    if event["requestContext"]["http"]["method"] == "GET":
        logger.info('Received get person request')
        person_id = event.get('queryStringParameters',{}).get('personId','')
        if not person_id:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "path":event["rawPath"],
                    "data": {
                        "message": "You need input personId in request",
                        "person":{}
                    }
                })
            }
        return {
            "statusCode": 200,
            "body": json.dumps({
                "path":event["rawPath"],
                "data": {
                    "message": "Retrieve successfully",
                    "person":{
                        "id": person_id,
                        "first name": "James",
                        "last name": "Bond",
                        "email": "jamesBond@example.com"
                    }
                }
            })
        }
    elif event["requestContext"]["http"]["method"] == "POST":
        logger.info('Received create person request')
        body = event.get("body",None)
        json_body = '' if not body else json.loads(body)
        if not json_body:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "path": event["rawPath"],
                    "data": {
                        "message": "You need to input info in request body",
                        "person":{}
                    }
                })
            }

        first_name = json_body.get('firstname')
        last_name = json_body.get('lastname')
        email = json_body.get('email')
        return {
            "statusCode": 201,
            "body":json.dumps({
                "path": event["rawPath"],
                "data":{
                    "message": "Created successfully",
                    "person":{
                        "id": uuid.uuid1().hex,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email
                    }
                }
            })
        }
    elif event["requestContext"]["http"]["method"] == "DELETE":
        logger.info('Received get person request')
        person_id = event.get('queryStringParameters',{}).get('personId','')
        if not person_id:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "path":event["rawPath"],
                    "data":{
                        "message": "You need put the personId in the request",
                        "person":{}
                    }
                })
            }
        return {
            "statusCode": 204,
            "body":json.dumps({
                "path": event["rawPath"],
                "data":{
                    "message": "Delete successfully",
                    "person":{}
                }
            })
        }
    elif event["requestContext"]["http"]["method"] == "PUT":
        logger.info('Received update person request')
        body = event.get("body", None)
        json_body = '' if not body else json.loads(body)
        if not json_body:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "path": event["rawPath"],
                    "data":{
                        "message": "You need to put the request body",
                        "person":{}
                    }
                })
            }
        first_name = json_body.get('firstname')
        last_name = json_body.get('lastname')
        email = json_body.get('email')
        return {
            "statusCode": 201,
            "body": json.dumps({
                "path": event["rawPath"],
                "data":{
                    "message": "Updated successfully",
                    "person":{
                        "id": uuid.uuid1().hex,
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email
                    }
                }
            })
        }
