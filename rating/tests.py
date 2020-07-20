from django.test import TestCase, Client
from model_mommy import mommy
from django.urls import reverse
import json

from .models import RatingProduct
from openfoodfacts.models import Product
from user.models import Profile
from django.contrib.auth.models import User


# Test views
class AddRatingProductTest(TestCase):

    def setUp(self):
        self.client = Client()
        # create user
        self.new_user = User.objects.create(username='test')
        self.new_user.set_password('test')
        self.new_user.save()
        # create profile linked to user
        self.new_profile = mommy.make(Profile, user=self.new_user)
        # create product
        self.product1 = mommy.make(Product, id=15, name="Perrier")

    def test_add_rating_product_save_new_rating(self):
        # fake user authentication
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('rating:add_rating_product', kwargs={'product_id': 15, 'rating': 4}))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 200)

    def test_add_rating_product_authentication_error(self):
        # test
        response = self.client.get(reverse('rating:add_rating_product', kwargs={'product_id': 15, 'rating': 3}))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 401)

    def test_add_rating_product_error_invalid_id(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('rating:add_rating_product', kwargs={'product_id': 9, 'rating': 4}))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 500)


class RemoveRatingProductTest(TestCase):

    def setUp(self):
        self.client = Client()
        # create user
        self.new_user = User.objects.create(username='test')
        self.new_user.set_password('test')
        self.new_user.save()
        # create profile linked to user
        new_profile = mommy.make(Profile, user=self.new_user)
        # create product
        self.product1 = mommy.make(Product, id=15, name="Perrier")
        # add one rating for a product
        mommy.make(RatingProduct, profile=new_profile, product=self.product1, rating=5)

    def test_remove_rating_product_ok(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('rating:remove_rating_product', kwargs={'product_id': 15}))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 200)

    def test_remove_rating_product_authentication_error(self):
        # test
        response = self.client.get(reverse('rating:remove_rating_product', kwargs={'product_id': 15}))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 401)

    def test_remove_rating_product_error_invalid_id(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('rating:remove_rating_product', kwargs={'product_id': 11}))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 500)


# Test models
class RatingProductTest(TestCase):

    def test_ratingproduct_creation(self):
        new_product = mommy.make(Product)
        new_ratingproduct = mommy.make(RatingProduct, product=new_product)
        self.assertTrue(isinstance(new_ratingproduct, RatingProduct))
        self.assertEqual(new_ratingproduct.product.name, new_product.name)
