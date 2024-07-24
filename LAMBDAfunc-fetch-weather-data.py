import typing
from fastapi import FastAPI, APIRouter, HTTPException
from mangum import Mangum
from boto3.dynamodb.types import TypeSerializer
import boto3, json

router = APIRouter()
app = FastAPI()

# Set up DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'weather_table'
table = dynamodb.Table(table_name)

@app.post("/")
async def save_to_dynamodb(request_body: dict):
    try:
        # Assume that the request body is a JSON object
        # Insert the data into the DynamoDB table and convert floats to stings
        nickname = request_body["nickname"]
        timestamp = request_body["timestamp"]
        request_body = request_body["readings"]
        for i in request_body:
            if isinstance(request_body[i], float):
                request_body[i] = str(request_body[i])
        request_body["nickname"] = nickname
        request_body["timestamp"] = timestamp
        response = table.put_item(Item=request_body)

        return 200

    except Exception as e:
        print("save_to_dynamodb fail", str(e), request_body)
        raise HTTPException(status_code=500, detail=str(e))

# Wrap the FastAPI app with Mangum for AWS Lambda compatibility
app.include_router(router, prefix="/api/v1") 
handler = Mangum(app)
