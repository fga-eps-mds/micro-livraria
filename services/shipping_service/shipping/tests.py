from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class ShippingRateTests(TestCase):
	# Configuração inicial para os testes
	def setUp(self):
		self.client = APIClient()
		self.url = reverse('get_shipping_rate')

	# Teste para verificar se a requisição GET retorna a taxa de envio corretamente
	def test_get_shipping_rate_success(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('value', response.data)
		self.assertIsInstance(response.data['value'], float)
		self.assertGreaterEqual(response.data['value'], 1.0)
		self.assertLessEqual(response.data['value'], 100.0)

	# Teste para verificar se a requisição POST não é permitida no endpoint
	def test_get_shipping_rate_invalid_method(self):
		response = self.client.post(self.url)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
