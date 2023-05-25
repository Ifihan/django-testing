from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
from django.test import TestCase, RequestFactory
from unittest.mock import Mock, patch
from .models import Name
from .views import name_list
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class HelloWorldViewTest(TestCase):
    def test_hello_world(self):
        url = reverse('accounts:hello_world')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Hello, world!")


class AddNumbersViewTest(TestCase):
    def test_add_numbers_get(self):
        url = reverse('accounts:add_numbers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please submit the form to add two numbers.")

    def test_add_numbers_post(self):
        url = reverse('accounts:add_numbers')
        data = {'num1': '5', 'num2': '3'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The sum of 5 and 3 is 8.")

class NameIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:name_list')

    def test_name_list_integration(self):
        # Create test data
        Name.objects.create(name='John', description='John Doe')
        Name.objects.create(name='Jane', description='Jane Smith')

        # Send a GET request to the URL
        response = self.client.get(self.url)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')
        self.assertContains(response, 'Jane')

class NameFunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super().setUp()

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_name_list_functional(self):
        # Create test data
        Name.objects.create(name='John', description='John Doe')
        Name.objects.create(name='Jane', description='Jane Smith')

        # Simulate user interactions using Selenium
        self.selenium.get(self.live_server_url + '/names/')
        self.assertIn('Name List', self.selenium.title)
        names =self.selenium.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0].text, 'John - John Doe')
        self.assertEqual(names[1].text, 'Jane - Jane Smith')

        # Simulate the page returns a 200
        self.assertEqual(self.selenium.title, 'Name List')


class NameListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_name_list_view(self):
        # Create some sample Name objects
        Name.objects.create(name='John Doe', description='Description 1')
        Name.objects.create(name='Jane Smith', description='Description 2')

        # Create a mock request object
        request = self.factory.get('/names/')

        # Create a mock queryset for the Name objects
        mock_queryset = Mock(spec=Name.objects.all())
        mock_queryset.return_value = [
            Mock(name='John Doe', description='Description 1'),
            Mock(name='Jane Smith', description='Description 2')
        ]

        # Patch the Name.objects.all() method to return the mock queryset
        with patch('account.views.Name.objects.all', mock_queryset):
            # Call the name_list view
            response = name_list(request)

        # Assert that the response has the expected status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected data
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Smith')
