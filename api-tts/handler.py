import json
import boto3
import hashlib
import datetime

# Inicializa a sessão boto3 e cria recursos para DynamoDB, Polly e S3
session = boto3.Session()
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('Nomedasuatabela')
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
        
        # Gera um ID único para a frase
        unique_id = generate_unique_id(phrase)

        # Verifica se a frase já foi processada anteriormente
        existing_item = get_from_dynamodb(unique_id)

        if existing_item:
            # Se a frase já existe, retorna os dados existentes
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "received_phrase": existing_item['received_phrase'],
                    "url_to_audio": existing_item['url_to_audio'],
                    "created_audio": existing_item['created_audio'],
                    "unique_id": unique_id
                }, indent=4)
            }
        else:
            # Gera o áudio e armazena no S3
            audio_url = generate_audio_and_store_in_s3(phrase, unique_id)

            # Salva os dados no DynamoDB
            save_to_dynamodb(phrase, unique_id, audio_url)

            # Retorna a resposta com os dados recém-criados
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "received_phrase": phrase,
                    "url_to_audio": audio_url,
                    "created_audio": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                    "unique_id": unique_id
                }, indent=4)
            }

# Função para gerar um ID único para a frase
def generate_unique_id(phrase):
    hash_object = hashlib.sha256(phrase.encode())
    return hash_object.hexdigest()[:6]

# Função para gerar áudio e armazenar no S3
def generate_audio_and_store_in_s3(phrase, unique_id):
    response = polly.synthesize_speech(
        Text=phrase,
        OutputFormat='mp3',
        VoiceId='Camila'
    )

    audio_key = f'audio-{unique_id}.mp3'
    s3.put_object(Bucket='nomedobucket', Key=audio_key, Body=response['AudioStream'].read())

    return f'https://nomedobucket.s3.amazonaws.com/{audio_key}'

# Função para salvar dados no DynamoDB
def save_to_dynamodb(phrase, unique_id, audio_url):
    table.put_item(
        Item={
            'unique_id': unique_id,
            'received_phrase': phrase,
            'url_to_audio': audio_url,
            'created_audio': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
    )

# Função para obter dados do DynamoDB
def get_from_dynamodb(unique_id):
    response = table.get_item(
        Key={
            'unique_id': unique_id
        }
    )

    return response.get('Item')
