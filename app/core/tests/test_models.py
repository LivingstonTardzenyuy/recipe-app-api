"""
    Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

# from .models import User


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'test123'
        User = get_user_model() 
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))    # we do like this b/c the password is being hashed
        

    def test_new_user_email_normalize(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['Test3@example.com', 'Test3@example.com'],
            # ['TEST4@example.com', 'Test4@example.com'],
            ['Test5@EXAMPLE.COM', 'Test5@example.com'],
        ]
        User = get_user_model() 
        for email, expected in sample_emails:
            user = User.objects.create_user(email, 'saple123')  # email and password.
            self.assertEqual(user.email, expected) 
    
    def test_new_user_without_email_raises_error(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'test123')
    
    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('admin@gmail.com', 'test123')
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        