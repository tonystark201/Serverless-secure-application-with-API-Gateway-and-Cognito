import uuid
import logging
logger = logging.getLogger()


def lambda_handler(event, context):
    if event["requestContext"]["http"]["method"] == "GET":
        return {
            "statusCode": 200,
            "body": "[GET METHOD]Hello,world"
        }
    elif event["requestContext"]["http"]["method"] == "POST":
        return {
            "statusCode": 200,
            "body": "[POST METHOD]Hello,world"
        }
    elif event["requestContext"]["http"]["method"] == "DELETE":
        return {
            "statusCode": 200,
            "body": "[DELTE METHOD]Hello,world"
        }
    elif event["requestContext"]["http"]["method"] == "PUT":
        return {
            "statusCode": 200,
            "body": "[PUT METHOD]Hello,world"
        }