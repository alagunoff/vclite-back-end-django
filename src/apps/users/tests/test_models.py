from rest_framework.test import APITestCase

from apps.users.models import User


class UserModelTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(
            username='artem', password='1234', first_name='Artem')
        User.objects.create_user(
            username='ivan', password='1234', first_name='Ivan')

    def test_str(self):
        artem = User.objects.get(username='artem')

        self.assertEqual(str(artem), artem.username)

    def test_is_staff_equal_to_is_admin(self):
        artem = User.objects.get(username='artem')
        self.assertEqual(artem.is_staff, artem.is_admin)

        ivan = User.objects.get(username='ivan')
        self.assertEqual(ivan.is_staff, ivan.is_admin)

    def test_superuser_is_both_admin_and_superuser(self):
        artem = User.objects.get(username='artem')

        self.assertTrue(artem.is_admin)
        self.assertTrue(artem.is_superuser)

    def test_user_is_neither_admin_nor_superuser(self):
        ivan = User.objects.get(username='ivan')

        self.assertFalse(ivan.is_admin)
        self.assertFalse(ivan.is_superuser)

    def test_username_max_length(self):
        artem = User.objects.get(username='artem')

        self.assertEqual(artem._meta.get_field('username').max_length, 30)

    def test_last_name_value(self):
        ivan = User.objects.get(username='ivan')

        self.assertIsNone(ivan.last_name)

    def test_is_admin_default(self):
        ivan = User.objects.get(username='ivan')

        self.assertFalse(ivan._meta.get_field('is_admin').default)
