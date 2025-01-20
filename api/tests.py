from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient

client = APIClient()
response = client.get('/api/get-userid/', data={'username': 'john_doe'})
