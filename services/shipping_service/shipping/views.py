from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

@api_view(['GET'])
def get_shipping_rate(request):
    # Gera um valor de frete aleatório entre R$1 e R$100
    shipping_value = round(random.uniform(1.0, 100.0), 2)
    
    # Retorna como resposta JSON
    return Response({'value': shipping_value})
