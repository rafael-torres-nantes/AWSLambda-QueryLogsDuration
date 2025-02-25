from decimal import Decimal
from statistics import mean

# Método para calcular a média de duração
def calculate_average_duration(items):
    """
    Calcula a média do valor da chave 'duration' em todos os itens da tabela.
    
    :return: Média das durações ou None se não houver dados
    """

    if not items:
        return None
    
    # Extrai os valores de duração de todos os itens que têm essa chave
    durations = []
    for item in items:
        
        if 'execution_time' in item:
            # Converte para número, se necessário
            duration = item['execution_time']
            
            if isinstance(duration, Decimal):
                duration = float(duration)
            
            elif isinstance(duration, str):
                
                try:
                    h, m, s = map(int, duration.split(':'))
                    duration = h * 3600 + m * 60 + s
                
                except ValueError:
                    print(f"Valor de duração inválido: {duration}")
                    continue
            
            durations.append(duration)
    
    if not durations:
        return None
    
    # Calcula a média das durações em segundos
    avg_duration = mean(durations)
    return avg_duration