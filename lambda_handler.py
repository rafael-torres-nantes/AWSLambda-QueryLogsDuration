import json
import os
from dotenv import load_dotenv

# Importa a função de cálculo de média de duração e a classe DynamoDB
from controller.calculate_execution_time import calculate_average_duration
from services.dynamodb_services import DynamoDBClass

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o nome da tabela DynamoDB do arquivo .env
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

def lambda_handler(event, context):
    """
    Lambda handler que consulta a média de duração no DynamoDB.
    
    :param event: Evento que acionou a função Lambda
    :param context: Contexto de execução da função Lambda
    :return: Resposta com a média de duração calculada
    """
    try:
   
        # Extrai parâmetros de filtro do evento, se houver
        filter_params = event.get('filter_params', {})
        
        # Inicializa a classe DynamoDB
        dynamo_service = DynamoDBClass(DYNAMODB_TABLE_NAME)

        # Obtém todos os itens da tabela DynamoDB
        items = dynamo_service.scan_table()
        print(f'[DEBUG] Itens encontrados: {len(items)}')

        # Calcula a média de duração dos itens em segundos
        avg_duration = calculate_average_duration(items)
        print(f'[DEBUG] Duração média: {avg_duration} seg')

        # Retorna a resposta com a média de duração calculada
        if avg_duration is not None:
            response = {
                'statusCode': 200,
                'body': json.dumps({
                    'average_duration': avg_duration,
                    'unit': 'seg',  # Unidade de medida (segundos)
                    'count': len(items),
                    'filters_applied': filter_params if filter_params else "None"
                })
            }	

        else:
            response = {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Nenhum dado de duração encontrado para calcular a média',
                    'filters_applied': filter_params if filter_params else "None"
                })
            }
        
        return response
        
        
#         # Prepara expressões de filtro se necessário
#         filter_expression = None
#         expression_attribute_values = None
        
#         if filter_params:
#             # Exemplos de parâmetros de filtro:
#             # - Filtragem por período: 'start_date' e 'end_date'
#             # - Filtragem por status: 'status'
            
#             filters = []
#             expression_attribute_values = {}
            
#             if 'start_date' in filter_params and 'end_date' in filter_params:
#                 filters.append("timestamp BETWEEN :start_date AND :end_date")
#                 expression_attribute_values[':start_date'] = filter_params['start_date']
#                 expression_attribute_values[':end_date'] = filter_params['end_date']
            
#             if 'status' in filter_params:
#                 filters.append("status = :status")
#                 expression_attribute_values[':status'] = filter_params['status']
            
#             # Verifica se há filtros para aplicar
#             if filters:
#                 filter_expression = " AND ".join(filters)
        
#         # Calcula a média de duração
#         avg_duration = dynamo_service.calculate_average_duration(
#             filter_expression=filter_expression,
#             expression_attribute_values=expression_attribute_values
#         )
        
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Erro ao processar a requisição: {str(e)}'
            })
        }

# Para teste local
if __name__ == "__main__":
    # Exemplo de evento para teste
    test_event = {
        'filter_params': {
            'status': 'completed'
        }
    }
    
    # Executa o handler com o evento de teste
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=4))
