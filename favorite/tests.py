from django.test import TestCase, Client
from model_mommy import mommy
from django.urls import reverse

from .models import Favorite
from .views import favorites
from .templatetags.favorite_filter import check_product_favorite

from user.models import Profile
from django.contrib.auth.models import User
from openfoodfacts.models import Product

import json


# Test views
class FavoritesTest(TestCase):

    def setUp(self):
        self.client = Client()
        # create user
        self.new_user = User.objects.create(username='test')
        self.new_user.set_password('test')
        self.new_user.save()
        # create profile linked to user
        new_profile = mommy.make(Profile, user=self.new_user)
        # create some products
        self.product1 = mommy.make(Product, name="Perrier")
        self.product2 = mommy.make(Product, name="Beurre sans gluten")
        self.product3 = mommy.make(Product, name="Pizza bio")
        # add some of the products as favorites
        self.favorite1 = mommy.make(Favorite, profile=new_profile, product=self.product1)
        self.favorite2 = mommy.make(Favorite, profile=new_profile, product=self.product2)

    def test_favorites_returns_product(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('favorite:favorites'))
        res_favorites = response.context['favorites']
        res_products = [Product.objects.get(id=f.product.id) for f in res_favorites]
        self.assertEqual(len(res_favorites), 2)
        self.assertIn(self.product1, res_products)
        self.assertNotIn(self.product3, res_products)


class AddFavoriteTest(TestCase):

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

    def test_add_favorite_save_new_favorite(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('favorite:add_favorite', kwargs={'substitute_product_id': 15 }))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 200)

    def test_add_favorite_authentication_error(self):
        # test
        response = self.client.get(reverse('favorite:add_favorite', kwargs={'substitute_product_id': 15 }))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 401)
    
    def test_add_favorite_error_duplicate_favorite(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('favorite:add_favorite', kwargs={'substitute_product_id': 9 }))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 500)


class RemoveFavoriteTest(TestCase):

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
          # add one product as favorites
        mommy.make(Favorite, profile=new_profile, product=self.product1)

    def test_remove_favorite_delete_favorite(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('favorite:remove_favorite', kwargs={'product_id': 15 }))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 200)
    
    def test_remove_favorite_authentication_error(self):
        # test
        response = self.client.get(reverse('favorite:remove_favorite', kwargs={'product_id': 15 }))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 401)

    def test_remove_favorite_error_invalid_id(self):
        # fake user authenticated
        login = self.client.login(username='test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('favorite:remove_favorite', kwargs={'product_id': 11 }))
        content = json.loads(response.content)
        self.assertEqual(content['status'], 500)


# Test models
class FavoriteTest(TestCase):
    
    def test_favorite_creation(self):
        new_product = mommy.make(Product)
        new_favorite = mommy.make(Favorite, product=new_product)
        self.assertTrue(isinstance(new_favorite, Favorite))
        self.assertEqual(new_favorite.__str__(), new_product.name)


# Test templatetags
class CheckProductFavoriteTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        # create user
        self.new_user = User.objects.create(username='test')
        self.new_user.set_password('test')
        self.new_user.save()
        # create profile linked to user
        self.new_profile = mommy.make(Profile, user=self.new_user)
        # create some products
        self.product1 = mommy.make(Product, name="Perrier", id=7)
        self.product2 = mommy.make(Product, name="Beurre sans gluten", id=9)
        # add some of the products as favorites
        self.favorite1 = mommy.make(Favorite, profile=self.new_profile, product=self.product1)

    def test_check_favorite_returns_true(self):
        result = check_product_favorite(7, self.new_user)
        self.assertTrue(result)

    def test_check_favorite_returns_false(self):
        result = check_product_favorite(9, self.new_user)
        self.assertFalse(result)
