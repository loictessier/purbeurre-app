from django.test import TestCase, Client
from unittest.mock import patch
from model_mommy import mommy
from django.urls import reverse

from .models import Profile
from .views import authentication
from .forms import AuthenticationForm, SignUpForm, AccountForm
from django.contrib.auth.models import User


# Test views
class AuthenticationTest(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.new_user = User.objects.create(username='test@test.test')
        self.new_user.set_password('test')
        self.new_user.save()

    def test_authentication_get(self):
        response = self.client.get(reverse('user:authentication'))
        self.assertFalse(response.context['error'])
 
    def test_authentication_post_valid(self):
        response = self.client.post(reverse('user:authentication'), {
            'username': 'test@test.test',
            'password': 'test'
        })
        self.assertFalse(response.context['error'])

    def test_authentication_post_user_invalid(self):
        response = self.client.post(reverse('user:authentication'), {
            'username': 'toto@toto.toto',
            'password': 'toto'
        })
        self.assertTrue(response.context['error'])

    def test_authentication_post_form_invalid(self):
        response = self.client.post(reverse('user:authentication'), {
            'username': 'toto',
            'password': 'toto'
        })
        self.assertTrue(response.context['error'])


class SignUpTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup_get(self):
        response = self.client.get(reverse('user:signup'))
        self.assertFalse(response.context['error'])

    def test_signup_post_valid_redirect(self):
        response = self.client.post(reverse('user:signup'), {
            'email': 'test@test.test',
            'password': 'test',
            'confirm_password': 'test'
        })
        self.assertEqual(response.status_code, 302)

    def test_signup_post_form_invalid(self):
        response = self.client.post(reverse('user:signup'), {
            'email': 'test@test.test',
            'password': 'test',
            'confirm_password': 't'
        })
        self.assertTrue(response.context['error'])


class AccountTest(TestCase):

    def setUp(self):
        self.client = Client()
        # create fake user
        self.new_user = User.objects.create(username='test@test.test')
        self.new_user.set_password('test')
        self.new_user.save()
        # create fake profile linked to user
        new_profile = mommy.make(Profile, user=self.new_user)

    def test_Account_valid(self):
         # fake user authenticated
        login = self.client.login(username='test@test.test', password='test')
        self.assertTrue(login)
        # test
        response = self.client.get(reverse('user:account'))
        self.assertFalse(response.context['error'])

    def test_account_invalid_not_authentified(self):
         # test
        response = self.client.get(reverse('user:account'))
        self.assertTrue(response.context['error'])


# Test models
class ProfileTest(TestCase):
    def test_profile_creation(self):
        new_user = mommy.make(User)
        new_profile = mommy.make(Profile, user=new_user)
        self.assertTrue(isinstance(new_profile, Profile))
        self.assertEqual(new_user.username, new_profile.__str__())


# Test forms
class AuthenticationFormTest(TestCase):

    def test_AuthenticationForm_valid(self):
        form = AuthenticationForm(data={'username': 'test@test.test', 'password': 'test'})
        self.assertTrue(form.is_valid())

    def test_AuthenticationForm_invalid(self):
        form = AuthenticationForm(data={'username': 'test', 'password': 'test'})
        self.assertFalse(form.is_valid())


class SignUpFormTest(TestCase):

    def test_SignUpForm_valid(self):
        form = SignUpForm(data={'email': 'test@test.test', 'password': 'test', 'confirm_password': 'test'})
        self.assertTrue(form.is_valid())

    def test_SignUpForm_invalid(self):
        form = SignUpForm(data={'email': 'test@test.test', 'password': 'test', 'confirm_password': 't'})
        self.assertFalse(form.is_valid())