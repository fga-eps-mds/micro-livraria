import json, os
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def search_all_products(request):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', 'products.json')

    with open(file_path, 'r') as file:
        data = json.load(file)
    return Response(data)