"""
    Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model



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
            ['test3@example.com', 'Test3@example.com'],
            ['TEST4@example.com', 'Test4@example.com'],
            ['test5@EXAMPLE.COM', 'Test5@example.com'],
        ]
        User = get_user_model() 
        for email, expected in sample_emails:
            user = User.objects.create_user(email, 'saple123')
            self.assertEqual(user.email, expected) 