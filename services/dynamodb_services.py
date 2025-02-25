# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ #

import boto3
import datetime
from botocore.exceptions import ClientError

class DynamoDBClass: 
    def __init__(self, dynamodb_table_name):
        """
        Construtor da classe DynamoDBClass que inicializa o cliente DynamoDB da sessão.
        """

        # Criação de nome da Dynamo Table
        self.dynamodb_table_name = dynamodb_table_name

        # Inicializa o cliente DynamoDB da sessão
        self.dynamodb = session.resource('dynamodb', region_name='us-east-1')

    
    # Serviço de DynamoDB de cadastro de log
    def log_register_dynamodb(self, unique_id):
        """
        Registra um log no DynamoDB contendo informações da requisição e resposta.

        :param request: Dados da requisição
        :return: None
        """
        # Inicia o serviço de DynamoDB e acessa a tabela especificada
        table = self.dynamodb.Table(self.dynamodb_table_name)  

        # Configura os dados do log
        log_item = {
            'unique_id': unique_id,
            'status' : 'false',
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
            
        try: # Insere os dados do log na tabela do DynamoDB
            table.put_item(Item=log_item)
            print("Dados do log inseridos no DynamoDB com sucesso")
        
        except ClientError as e: # Caso ocorra um erro, imprime a mensagem de erro
            print(f"Erro ao inserir os dados do log no DynamoDB: {e}")
            
    # Método para buscar o item no DynamoDB pelo ID
    def get_item(self, unique_id):
        """
        Obtém um item do DynamoDB pelo ID fornecido.
        :param unique_id: ID do item a ser buscado
        :return: Dicionário com os dados do item encontrado
        """
        # Inicia o serviço de DynamoDB e acessa a tabela especificada
        table = self.dynamodb.Table(self.dynamodb_table_name)
        
        try: # Busca o item no DynamoDB pelo ID fornecido
            response = table.get_item(Key={'unique_id': unique_id})
            return response.get('Item', {})
            
        except ClientError as e: # Caso ocorra um erro, retorna None
            print(f"Erro ao buscar o item no DynamoDB: {e}")
            return None
    
    # Método para remover o item no DynamoDB pelo ID
    def delete_item(self, unique_id):
        """
        Remove um item do DynamoDB pelo ID fornecido.
        :param unique_id: ID do item a ser removido
        :return: Dicionário com os dados do item removido
        """
        # Inicia o serviço de DynamoDB e acessa a tabela especificada
        table = self.dynamodb.Table(self.dynamodb_table_name)
        
        try: # Remove o item no DynamoDB pelo ID fornecido
            response = table.delete_item(Key={'unique_id': unique_id})
            return response.get('Item', {})
            
        except ClientError as e: # Caso ocorra um erro, retorna None
            print(f"Erro ao remover o item no DynamoDB: {e}")
            return None
    
    # Método para atualizar um item no DynamoDB
    def update_item(self, unique_id, update_data):
        """
        Atualiza um item no DynamoDB com os dados fornecidos.
        
        :param unique_id: ID do item a ser atualizado
        :param update_data: Dicionário com os dados a serem atualizados
        :return: Response da operação de atualização
        """
        table = self.dynamodb.Table(self.dynamodb_table_name)
        
        # Constrói a expressão de atualização
        update_expression = "SET "
        expression_attribute_values = {}
        
        for key, value in update_data.items():
            update_expression += f"{key} = :{key.replace('.', '_')}, "
            expression_attribute_values[f":{key.replace('.', '_')}"] = value
        
        # Remove a vírgula e o espaço no final
        update_expression = update_expression[:-2]
        
        try:
            response = table.update_item(
                Key={'unique_id': unique_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )
            return response
            
        except ClientError as e:
            print(f"Erro ao atualizar o item no DynamoDB: {e}")
            return None
    
    # Método para escanear a tabela completa
    def scan_table(self, filter_expression=None, expression_attribute_values=None):
        """
        Escaneia a tabela DynamoDB completa com filtros opcionais.
        
        :param filter_expression: Expressão de filtro opcional
        :param expression_attribute_values: Valores de atributo da expressão opcional
        :return: Lista com todos os itens encontrados
        """
        table = self.dynamodb.Table(self.dynamodb_table_name)
        items = []
        
        try:
            scan_kwargs = {}
            if filter_expression:
                scan_kwargs['FilterExpression'] = filter_expression
            if expression_attribute_values:
                scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values
            
            response = table.scan(**scan_kwargs)
            items.extend(response.get('Items', []))
            
            # Paginação: continua o scan se houver mais itens
            while 'LastEvaluatedKey' in response:
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = table.scan(**scan_kwargs)
                items.extend(response.get('Items', []))
                
            return items
            
        except ClientError as e:
            print(f"Erro ao escanear a tabela DynamoDB: {e}")
            return []
    
    # Método para consulta com base em um índice secundário
    def query_by_index(self, index_name, key_condition_expression, expression_attribute_values):
        """
        Realiza uma consulta usando um índice secundário.
        
        :param index_name: Nome do índice secundário
        :param key_condition_expression: Expressão de condição de chave
        :param expression_attribute_values: Valores de atributo da expressão
        :return: Lista com os itens encontrados
        """
        table = self.dynamodb.Table(self.dynamodb_table_name)
        items = []
        
        try:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            
            items.extend(response.get('Items', []))
            
            # Paginação: continua a consulta se houver mais itens
            while 'LastEvaluatedKey' in response:
                response = table.query(
                    IndexName=index_name,
                    KeyConditionExpression=key_condition_expression,
                    ExpressionAttributeValues=expression_attribute_values,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                items.extend(response.get('Items', []))
                
            return items
            
        except ClientError as e:
            print(f"Erro ao consultar o índice no DynamoDB: {e}")
            return []