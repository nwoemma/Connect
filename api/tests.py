from django.test import TestCase
from django.urls import reverse
from django.test import Client
import pickle
# Create your tests here.
class TestCase_for_connect(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:chat_response')  
    #     self.user = {
    #         'email':'nwosuemmanuel159@gmail.com',
    #         'password':'password123',
    #     }
    def test_chat_response(self):
        # Send pickled data as expected by your view
        data = {'messages': 'Hello'}
        pickled_data = pickle.dumps(data)

        response = self.client.post(
            self.url,
            pickled_data,
            content_type='application/octet-stream'  # Important for binary data
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
        self.assertIsInstance(response.json()['response'], str)
    