from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TaskFilterTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='task-filter-user')
        self.client.force_authenticate(user=user)
        self.url = reverse('api:task-list')

    def test_numeric_filters_reject_invalid_values(self):
        for key in ('plan', 'section', 'priority'):
            for value in ('abc', '', '1.5'):
                with self.subTest(key=key, value=value):
                    response = self.client.get(self.url, {key: value})

                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                    self.assertIn(key, response.data)

    def test_numeric_filters_accept_integers(self):
        for key in ('plan', 'section', 'priority'):
            with self.subTest(key=key):
                response = self.client.get(self.url, {key: '1'})

                self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:user-list')
        self.payload = {
            'username': 'new-user',
            'password': 'N3w-Quite-Long-Secret!',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new.user@example.test',
        }

    def test_registration_hashes_password_and_returns_no_password(self):
        response = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        user = get_user_model().objects.get(username=self.payload['username'])
        self.assertEqual(user.first_name, self.payload['first_name'])
        self.assertEqual(user.last_name, self.payload['last_name'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)

    def test_registration_requires_snake_case_name_fields(self):
        payload = self.payload.copy()
        payload['firstName'] = payload.pop('first_name')
        payload['lastName'] = payload.pop('last_name')

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    def test_registration_rejects_weak_password(self):
        payload = self.payload.copy()
        payload['password'] = 'password'

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(get_user_model().objects.filter(username=payload['username']).exists())

    def test_user_detail_does_not_expose_password(self):
        user = get_user_model().objects.create_user(
            username='existing-user',
            password=self.payload['password'],
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('api:user-detail', kwargs={'pk': user.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

    def test_user_detail_cannot_change_superuser_status(self):
        user = get_user_model().objects.create_user(
            username='regular-user',
            password=self.payload['password'],
        )
        self.client.force_authenticate(user=user)

        response = self.client.patch(
            reverse('api:user-detail', kwargs={'pk': user.pk}),
            {'is_superuser': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertFalse(user.is_superuser)
