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
    
    return {
            'statusCode': 200,
            'body': json.dumps("Hello from Lambda")
        }