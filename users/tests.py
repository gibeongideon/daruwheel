from django.test import TestCase  #,Client
from django.urls import reverse
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test_user", email="test@gmail.com")
      
    def test_user_creation(self):

        """Create user """
        user = User.objects.get(username="test_user")
        self.assertEqual(user.username, 'test_user')