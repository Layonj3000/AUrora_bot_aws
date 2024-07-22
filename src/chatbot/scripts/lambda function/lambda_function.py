import json
import re

import pymysql
from cancel_appointment import cancel_appointment
from fetch_appointments import fetch_appointments
from insert_into_db import insert_into_db

# Configurações do banco de dados
db_config = {
    'host': 'HOST',
    'user': 'USER',
    'password': 'PASSWORD',
    'database': 'DATABASE'
}

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
    
def lambda_handler(event, context):  
    try:
        intent_name = event['sessionState']['intent']['name']
        slots = event['sessionState']['intent']['slots']
        print("Intent name:", intent_name)
        print("Slots:", json.dumps(slots))

        def remove_mailto(text):
            pattern = r'<mailto:(.*?\|)(.*?)>'
            result = re.sub(pattern, r'\2', text)
            return result
        
        def is_valid_email(email):
            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            return re.match(pattern, email) is not None

        if intent_name == 'AgendarConsulta':
            
            if event['invocationSource'] == 'FulfillmentCodeHook':
                data = {
                    'nome': slots['nome']['value']['interpretedValue'],
                    'celular': slots['celular']['value']['interpretedValue'],
                    'nomeAnimal': slots['nomeAnimal']['value']['interpretedValue'],
                    'email': slots['email']['value']['originalValue'],
                    'especie': slots['especie']['value']['interpretedValue'],
                    'data': slots['data']['value']['interpretedValue'],
                    'horario': slots['horario']['value']['interpretedValue']
                }
                print("Preparando para inserir no banco de dados")
                
                email_novo = remove_mailto(data['email'])
                if is_valid_email(email_novo):
                    print("Email validado:", email_novo)
                    data['email'] = email_novo
                else:
                    print("Email inválido:", email_novo)

                    return elicit_slot(event['sessionState']['sessionAttributes'], intent_name, slots, 'email', f' O e-mail digitado não é válido. Insira um e-mail válido.')
                    
                response = insert_into_db(data)
                if response['statusCode'] == 200:
                    return close(event, 'Fulfilled', 'Consulta marcada com sucesso')
                else:
                    return close(event, 'Failed', 'Erro ao inserir os dados no banco de dados.')
            else:
                return delegate(event)
            
        if intent_name == 'BuscarConsulta':
   
            if event['invocationSource'] == 'FulfillmentCodeHook':
                data = {
                    'email': slots['email']['value']['interpretedValue']
                }
                
                email_novo = remove_mailto(data['email'])
                
                if is_valid_email(email_novo):
                    print("Email validado:", email_novo)
                    data['email'] = email_novo
                else:
                    print("Email inválido:", email_novo)

                    return elicit_slot(event['sessionState']['sessionAttributes'], intent_name, slots, 'email', f'Insira um email válido.')
                
                response = fetch_appointments(data)
                if response['statusCode'] == 200:
                    message = json.loads(response['body'])
                    return close(event, 'Fulfilled', message)
                elif response['statusCode'] == 404:
                    return close(event, 'Failed', 'Nenhuma consulta encontrada para o email fornecido.')
                else:
                    return close(event, 'Failed', 'Erro ao buscar as consultas no banco de dados.')

            else:
                return delegate(event)
        if intent_name == 'DesmarcarConsulta':
                if event['invocationSource'] == 'FulfillmentCodeHook':
                    data = {
                        'email': slots['email']['value']['interpretedValue'],
                        'pet_id': slots['pet_id']['value']['interpretedValue'],
                        'appointment_id': slots['appointment_id']['value']['interpretedValue']
                    }
                    
                    email_novo = remove_mailto(data['email'])
                    
                    if is_valid_email(email_novo):
                        print("Email validado:", email_novo)
                        data['email'] = email_novo
                    else:
                        print("Email inválido:", email_novo)
                        return elicit_slot(event['sessionState']['sessionAttributes'], intent_name, slots, 'email', f'Insira um email válido.')
                        
                    
                    response = cancel_appointment(data)
                    if response['statusCode'] == 200:
                        return close(event, 'Fulfilled', 'Consulta cancelada com sucesso')
                    elif response['statusCode'] == 404:
                        return close(event, 'Failed', 'Consulta não encontrada.')
                    else:
                        return close(event, 'Failed', 'Erro ao cancelar a consulta no banco de dados.')
                else:
                    return delegate(event)
                
        return close(event, 'Failed', 'Erro ao processar a intenção.')
                
    except Exception as e:
        print(f"Erro geral no Lambda: {str(e)}")
        return close(event, 'Failed', f"Erro ao processar a intenção: {str(e)}")
    
    
