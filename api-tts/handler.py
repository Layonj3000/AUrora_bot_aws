import json
import boto3

# Inicializa a sessão boto3 e cria recursos para DynamoDB, Polly e S3
session = boto3.Session()
dynamodb = session.resource('dynamodb')
polly = session.client('polly')
s3 = session.client('s3')

def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v1_description(event, context):
    body = {
        "message": "TTS api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def text_to_speech(event, context):
   try:
        if 'body' in event:
            # Faz o parse do corpo da requisição JSON
            body = json.loads(event['body'])
        else:
            body = {}

        # Obtém a frase da requisição
        phrase = body.get('phrase')

        if not phrase:
            # Retorna um erro se a frase não for fornecida
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Frase não fornecida"
                })
            }