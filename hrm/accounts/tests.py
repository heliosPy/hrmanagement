from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTest(TestCase):
    """To test the custom user methods like create_staff, create_applicant etc all method from custonusermanager"""

    def test_create_user(self):
        """Testing the user who is applicant"""
        User = get_user_model()
        user = User.objects.create_user(email='user@gmail.com', password='testpass')
        self.assertEqual(user.email, 'user@gmail.com')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_applicant)
        self.assertEqual(user.get_full_name(), 'user@gmail.com')
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_create_staff(self):
        """Testing the user who is staff"""
        User = get_user_model()
        user = User.objects.create_staff(email='staff1@gmail.com', password='testpass')
        self.assertEqual(user.email, 'staff1@gmail.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_applicant)
        self.assertEqual(user.get_full_name(), 'staff1@gmail.com')
        with self.assertRaises(TypeError):
            User.objects.create_staff()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_create_superuser(self):
        """Testing the user who is an superuser"""
        User = get_user_model()
        user = User.objects.create_superuser(email='superuser@gmail.com', password='testpass')
        self.assertEqual(user.email, 'superuser@gmail.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_applicant)
        self.assertEqual(user.get_full_name(), 'superuser@gmail.com')
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")





