from django.test import TestCase
import json
from pathlib import Path

class ProductTests(TestCase):
	def setUp(self):
		# Carregar os produtos do arquivo JSON
		products_file = Path(__file__).resolve().parent.parent / 'products.json'
		try:
			with open(products_file) as file:
				self.products = json.load(file)
		except FileNotFoundError:
			self.fail(f"File {products_file} not found.")
		except json.JSONDecodeError:
			self.fail(f"File {products_file} is not a valid JSON.")

	def test_products_loaded(self):
		# Verificar se os produtos foram carregados corretamente
		self.assertIsInstance(self.products, list)
		self.assertGreater(len(self.products), 0)

	def test_product_structure(self):
		# Verificar a estrutura dos produtos
		for product in self.products:
			self.assertIn('id', product)
			self.assertIn('name', product)
			self.assertIn('author', product)
			self.assertIn('quantity', product)
			self.assertIn('price', product)
			self.assertIn('photo', product)
			self.assertIsInstance(product['id'], int)
			self.assertIsInstance(product['name'], str)
			self.assertIsInstance(product['author'], str)
			self.assertIsInstance(product['quantity'], int)
			self.assertIsInstance(product['price'], (int, float))
			self.assertIsInstance(product['photo'], str)