from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Testing customise User model """

    def test_create_user_with_email_successful(self):
        """Test creating new user with email successful """

        email = 'test@twysolutions.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """shoud normalized new email"""
        email = 'test@LATIFAPPDEV.COM'
        user = get_user_model().objects.create_user(email, password='test@123')
        self.assertEquals(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """should raise error if email is invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@123')

    def test_create_new_superuser(self):
        """should create new super user"""
        user = get_user_model().objects.create_superuser('superuser@eg.com', 'super@pass')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_new_staff(self):
        """should create new staff((admin)) user"""
        user = get_user_model().objects.create_staff('staffuser@eg.com', 'staff@pass')
        self.assertTrue(user.is_staff)

    def test_create_new_teacher(self):
        """should create new teacher user"""
        user = get_user_model().objects.create_teacher('teacheruser@eg.com', 'teacher@pass')
        self.assertTrue(user.is_teacher)

    def test_create_new_student(self):
        """should create new student user"""
        user = get_user_model().objects.create_student('studentuser@eg.com', 'student@pass')
        self.assertTrue(user.is_student)

    def test_create_new_parent(self):
        """should create new student user"""
        user = get_user_model().objects.create_parent('parentuser@eg.com', 'parent@pass')
        self.assertTrue(user.is_parent)
