import pymysql
import json
import re

# Configurações do banco de dados
db_config = {
    'host': 'HOST',
    'user': 'USER',
    'password': 'PASSWORD',
    'database': 'DATABASE'
}

def lambda_handler(event, context):

    def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
        print(f"Elicit slot {slot_to_elicit} with message: {message}")
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'slotToElicit': slot_to_elicit
                },
                'intent': {
                    'name': intent_name,
                    'slots': slots
                }
            },
            'messages': [{
                'contentType': 'PlainText',
                'content': message
            }]
        }
    
    def delegate(intent_request):
        print("delegate called")
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Delegate'
                },
                'intent': intent_request['sessionState']['intent']
            }
        }
    
        def close(intent_request, fulfillment_state, message):
        print("close called with message:", message)
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close'
                },
                'intent': {
                    'name': intent_request['sessionState']['intent']['name'],
                    'state': fulfillment_state
                }
            },
            'messages': [{
                'contentType': 'PlainText',
                'content': message
            }]
        }
    def insert_into_db(data):
        print("insert_into_db with data:", data)
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Inserir na tabela customers
                customer_query = '''
                INSERT INTO customers (email, first_name, phone) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE first_name=%s, phone=%s
                '''
                cursor.execute(customer_query, (data['email'], data['nome'], data['celular'], data['nome'], data['celular']))
        
    return {
            'statusCode': 200,
            'body': json.dumps("Hello from Lambda")
        }