from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.test.client import Client

from .form import CommentForm, ProductForm


class ViewTest(TestCase):
    def setUp(self):
        # Установки запускаются перед каждым тестом
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='admin', password='admin')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_index(self):
        # проверка открытия главной страницы
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        # проверка открытия  страницы о компании
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        # проверка открытия  страницы продуктов
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_contacts(self):
        # проверка открытия  страницы контакты
        response = self.client.get('/contacts')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # проверка открытия  страницы контакты
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_vacancies(self):
        # проверка открытия  страницы контакты
        response = self.client.get('/vacancies')
        self.assertEqual(response.status_code, 200)

    def test_authentication(self):
        user = authenticate(username='admin', password='admin')
        self.assertTrue((user is not None) and user.is_authenticated)


class FormTest(TestCase):
    def test_name_of_product_starting_lowercase(self):
        form = ProductForm(data={"name": "a lowercase name"})
        self.assertEqual(
            form.errors["name"], ["Должно начинаться с большой буквы"]
        )

    def test_description_of_product_short(self):
        form = ProductForm(data={"description": "short"})
        self.assertEqual(
            form.errors["description"], ['Слишком короткое описание. Описание должно содержать более 10 знаков!']
        )

    def test_price_of_product_high(self):
        form = ProductForm(data={"price": 100000})
        self.assertEqual(
            form.errors["price"], ['Некорректная цена!']
        )

    def test_name_of_comment_starting_lowercase(self):
        form = CommentForm(data={"last_name": "a lowercase last name"})
        self.assertEqual(
            form.errors["last_name"], ["Должно начинаться с большой буквы"]
        )
