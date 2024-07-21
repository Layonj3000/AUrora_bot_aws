import json
import re

import pymysql

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
            # Inserir na tabela pets, se não existir
                pet_query = '''
                INSERT INTO pets (customer_email, name_pet, species) 
                SELECT %s, %s, %s 
                FROM DUAL 
                WHERE NOT EXISTS (
                    SELECT * FROM pets WHERE customer_email = %s AND name_pet = %s AND species = %s
                )
                '''
                cursor.execute(pet_query, (data['email'], data['nomeAnimal'], data['especie'], data['email'], data['nomeAnimal'], data['especie']))
                # Obter o ID do pet
                cursor.execute('SELECT pet_id FROM pets WHERE customer_email = %s AND name_pet = %s AND species = %s', 
                               (data['email'], data['nomeAnimal'], data['especie']))
                pet_id = cursor.fetchone()[0]

                # Inserir na tabela appointments, se não existir
                appointment_query = '''
                INSERT INTO appointments (pet_id, customer_email, appointment_date) 
                SELECT %s, %s, %s 
                FROM DUAL 
                WHERE NOT EXISTS (
                    SELECT * FROM appointments WHERE pet_id = %s AND customer_email = %s AND appointment_date = %s
                )
                '''
                appointment_datetime = f"{data['data']} {data['horario']}"
                cursor.execute(appointment_query, (pet_id, data['email'], appointment_datetime, pet_id, data['email'], appointment_datetime))

            connection.commit()

        except pymysql.MySQLError as e:
            print(f"Erro ao inserir no banco de dados: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Erro ao inserir no banco de dados: {str(e)}")
            }
        finally:
            connection.close()
        print("inserido")
        return {
            'statusCode': 200,
            'body': json.dumps("Dados inseridos com sucesso")
        }
    


    def fetch_appointments(data):
        print("fetch_appointments with data:", data)
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Buscar consultas do cliente
                query = '''
                SELECT appointments.appointment_id, pets.pet_id, pets.name_pet, appointments.appointment_date 
                FROM appointments 
                JOIN pets ON appointments.pet_id = pets.pet_id 
                WHERE appointments.customer_email = %s
                '''
                cursor.execute(query, (data['email'],))
                appointments = cursor.fetchall()
                print("Resultados da consulta:", appointments)
            if not appointments:
                print("Nenhuma consulta encontrada para o email:", data['email'])
                return {
                    'statusCode': 404,
                    'body': json.dumps("Nenhuma consulta encontrada para o email fornecido.")
                }
    
            connection.commit()
            print("Consulta realizada com sucesso")

             # Converter datetime para string no formato brasileiro
            def format_datetime_br(datetime_str):
                from datetime import datetime
                dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                return dt.strftime('%d/%m/%Y %H:%M:%S')
    
            appointments = [(appointment[0], appointment[1], appointment[2], format_datetime_br(appointment[3].strftime('%Y-%m-%d %H:%M:%S'))) for appointment in appointments]
            print("Consultas formatadas:", appointments)
    
            # Criar a mensagem em formato de tabela com colunas alinhadas
            message = "Suas consultas:\n"
            message += "{:<16} | {:<10} | {:<15} | {:<20}\n".format("ID da Consulta", "ID do Pet", "Nome do Pet", "Data da Consulta")
            message += "-" * 65 + "\n"
            for appointment in appointments:
                message += "{:<25} | {:<17} | {:<15} | {:<20}\n".format(appointment[0], appointment[1], appointment[2], appointment[3])
    
            return {
                'statusCode': 200,
                'body': json.dumps(message)
            }
        except pymysql.MySQLError as e:
            print(f"Erro ao buscar consultas no banco de dados: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Erro ao buscar consultas no banco de dados: {str(e)}")
            }
        finally:
            if connection:
                connection.close()
                print("Conexão fechada")


    def cancel_appointment(data):
        print("cancel_appointment with data:", data)
        print(f"Email: {data['email']}, Pet ID: {data['pet_id']}, Appointment ID: {data['appointment_id']}")

        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Cancelar consulta
                query = '''
                DELETE a 
                FROM appointments a
                JOIN pets p ON a.pet_id = p.pet_id
                WHERE a.customer_email = %s AND p.pet_id = %s AND a.appointment_id = %s
                '''
                cursor.execute(query, (data['email'], data['pet_id'], data['appointment_id']))

            connection.commit()
            if cursor.rowcount > 0:
                return {
                    'statusCode': 200,
                    'body': json.dumps("Consulta cancelada com sucesso")
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps("Consulta não encontrada")
                }

        except pymysql.MySQLError as e:
            print(f"Erro ao cancelar consulta no banco de dados: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Erro ao cancelar consulta no banco de dados: {str(e)}")
            }
        finally:
            connection.close()
    
    
    
    
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

    except Exception as e:
        print(f"Erro geral no Lambda: {str(e)}")
        return close(event, 'Failed', f"Erro ao processar a intenção: {str(e)}")
    
    
    return {
            'statusCode': 200,
            'body': json.dumps("Hello from Lambda")
        }