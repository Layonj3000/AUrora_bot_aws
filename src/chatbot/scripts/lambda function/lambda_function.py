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

    return {
            'statusCode': 200,
            'body': json.dumps("Hello from Lambda")
        }