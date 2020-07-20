from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from model_mommy import mommy

from .views import index, get_products
from .models import Category, Product
from rating.models import RatingProduct

import json


# Test views
class IndexTest(TestCase):
    def test_root_url_resolve_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8').strip()
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Pur beurre</title>', html)
        self.assertIn('<strong>Du gras, oui, mais de qualité !</strong>', html)
        self.assertTrue(html.endswith('</html>'))


class GetProductsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        mommy.make(Product, id=1, name="coca", nutriscore="E")
        mommy.make(Product, id=30, name="coca light", nutriscore="E")
        mommy.make(Product, id=15, name="coca cherry", nutriscore="E")
        mommy.make(Product, id=11, name="orangina", nutriscore="E")

    def test_get_products_returns_products(self):

        class FakeRequest:
            def __init__(self, query):
                self.GET = {
                    'term': query
                }

            def is_ajax(self):
                return True

        request = FakeRequest("coca")
        response = get_products(request)
        self.assertEqual(3, len(json.loads(response.content)))
        self.assertIn("coca", str(json.loads(response.content)))
        self.assertIn("coca light", str(json.loads(response.content)))
        self.assertIn("coca cherry", str(json.loads(response.content)))
        self.assertNotIn("orangina", str(json.loads(response.content)))

    def test_get_products_returns_fail(self):

        class FakeRequest:
            def __init__(self, query):
                self.GET = {
                    'term': query
                }

            def is_ajax(self):
                return False

        request = FakeRequest("coca")
        response = get_products(request)
        self.assertEqual("fail", str(json.loads(response.content)))


class ResultsTest(TestCase):

    def setUp(self):
        self.client = Client()
        # create products
        c1 = mommy.make(Category, id=1, name="Boissons gazeuses")
        c2 = mommy.make(Category, id=2, name="Gateaux")
        p1 = mommy.make(Product, id=1, name="coca", nutriscore="E", category=c1)
        p2 = mommy.make(Product, id=30, name="Perrier", nutriscore="A", category=c1)
        p3 = mommy.make(Product, id=15, name="Badoit", nutriscore="A", category=c1)
        p4 = mommy.make(Product, id=11, name="orangina", nutriscore="E", category=c1)
        p5 = mommy.make(Product, id=55, name="Biscuit Bio", nutriscore="A", category=c2)
        p6 = mommy.make(Product, id=67, name="Gateau sans gluten", nutriscore="A", category=c2)
        # create ratings
        mommy.make(RatingProduct, product=p1, rating=1)
        mommy.make(RatingProduct, product=p2, rating=4)
        mommy.make(RatingProduct, product=p3, rating=3)
        mommy.make(RatingProduct, product=p4, rating=2)
        mommy.make(RatingProduct, product=p5, rating=4)
        mommy.make(RatingProduct, product=p6, rating=5)

    def test_results_returns_products(self):
        response = self.client.get(reverse('openfoodfacts:results'), {'search_input': 'Coca [E]'})
        self.assertEqual(len(response.context['results']), 4)
        self.assertIn("Perrier", str(response.context['results'].values()))
        self.assertNotIn("Biscuit Bio", str(response.context['results'].values()))
        self.assertTrue(response.context['status'])

    def test_results_returns_products_with_filter(self):
        response = self.client.get(reverse('openfoodfacts:results', kwargs={'rating_filter': 3}),
                                   {'search_input': 'Coca [E]'})
        self.assertEqual(len(response.context['results']), 2)
        self.assertIn("Perrier", str(response.context['results'].values()))
        self.assertNotIn("Biscuit Bio", str(response.context['results'].values()))
        self.assertTrue(response.context['status'])

    def test_results_returns_no_products(self):
        response = self.client.get(reverse('openfoodfacts:results'), {'search_input': 'not existing product'})
        self.assertEqual(len(response.context['results']), 0)
        self.assertFalse(response.context['status'])


class ProductDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        mommy.make(Product, id=33, name="test")

    def test_product_detail_returns_product(self):
        response = self.client.get(reverse('openfoodfacts:detail', kwargs={'product_id': 33}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result'].name, "test")

    def test_product_detail_raise_404(self):
        response = self.client.get(reverse('openfoodfacts:detail', kwargs={'product_id': 1}))
        self.assertEqual(response.status_code, 404)


# Test models
class CategoryTest(TestCase):
    def test_category_creation(self):
        c = mommy.make(Category)
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.name)


class ProductTest(TestCase):
    def test_product_creation(self):
        new_product = mommy.make('openfoodfacts.Product')
        self.assertTrue(isinstance(new_product, Product))
        self.assertEqual(new_product.__str__(), new_product.name)
