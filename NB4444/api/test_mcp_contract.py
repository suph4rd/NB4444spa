from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase
from PIL import Image

from B4.models import Note, Plan, Task, DefaultDeductions


class MCPContractTests(APITestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username='owner')
        self.other = get_user_model().objects.create_user(username='other')
        self.client.force_authenticate(self.owner)
        self.plan = Plan.objects.create(user=self.owner, name='plan')

    def test_crud_and_soft_delete(self):
        for endpoint, payload, patch, model in (
            ('note', {'text': 'note'}, {'text': 'updated'}, Note),
            ('plan', {'name': 'new'}, {'name': 'updated'}, Plan),
            ('task', {'plan': self.plan.pk, 'description': 'task'}, {'priority': 3}, Task),
            ('default-deduction', {'house': '12.30'}, {'house': '14.00'}, DefaultDeductions),
        ):
            with self.subTest(endpoint=endpoint):
                url = '/api/v1/' + endpoint + '/'
                response = self.client.post(url, payload, format='json')
                self.assertEqual(response.status_code, 201, response.data)
                pk = response.data['id']
                detail = f'{url}{pk}/'
                self.assertEqual(self.client.get(detail).status_code, 200)
                self.assertEqual(self.client.patch(detail, patch, format='json').status_code, 200)
                self.client.force_authenticate(self.other)
                self.assertEqual(self.client.get(detail).status_code, 404)
                self.assertEqual(self.client.patch(detail, patch, format='json').status_code, 404)
                self.assertEqual(self.client.delete(detail).status_code, 404)
                self.client.force_authenticate(self.owner)
                self.assertEqual(self.client.delete(detail).status_code, 204)
                self.assertFalse(model.objects.filter(pk=pk).exists())
                self.assertTrue(model.all_objects.get(pk=pk).is_delete)

    def test_list_pagination_owner_and_admin(self):
        Note.objects.create(user=self.owner, text='mine')
        Note.objects.create(user=self.other, text='other')
        Plan.objects.create(user=self.other, name='other')
        for endpoint in ('note', 'plan'):
            response = self.client.get(f'/api/v1/{endpoint}/', {'offset': 0, 'limit': 1})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['user']['id'], self.owner.pk)
        admin = get_user_model().objects.create_superuser(username='mcp-contract-admin', password='test')
        self.client.force_authenticate(admin)
        self.assertEqual(len(self.client.get('/api/v1/note/').data), 2)

    def test_deleted_plan_hides_tasks(self):
        task = Task.objects.create(plan=self.plan, description='task')
        self.plan.delete()
        self.assertEqual(self.client.get(f'/api/v1/task/{task.pk}/').status_code, 404)
        self.assertEqual(self.client.get('/api/v1/task/').data, [])

    def test_multipart_create_with_disk_upload(self):
        with TemporaryDirectory() as folder, override_settings(
            MEDIA_ROOT=folder, FILE_UPLOAD_MAX_MEMORY_SIZE=0,
        ):
            data = BytesIO()
            Image.new('RGB', (2, 2)).save(data, format='PNG')
            response = self.client.post('/api/v1/note/', {
                'text': 'photo', 'user': self.other.pk,
                'image': SimpleUploadedFile('test.png', data.getvalue(), 'image/png'),
            }, format='multipart')
            self.assertEqual(response.status_code, 201, response.data)
            self.assertEqual(Note.objects.get(pk=response.data['id']).user_id, self.owner.pk)

    def test_photos(self):
        with TemporaryDirectory() as folder, override_settings(MEDIA_ROOT=folder):
            note = Note.objects.create(user=self.owner, text='photo')
            url = f'/api/v1/note/{note.pk}/'
            self.assertEqual(self.client.get(url + 'image/').status_code, 404)
            data = BytesIO()
            Image.new('RGB', (2, 2)).save(data, format='PNG')
            response = self.client.patch(url, {'image': SimpleUploadedFile(
                'test.png', data.getvalue(), 'image/png')}, format='multipart')
            self.assertEqual(response.status_code, 200, response.data)
            response = self.client.get(url + 'image/')
            self.assertEqual(response.status_code, 200)
            response.close()
            self.assertEqual(len(self.client.get('/api/v1/note/', {'has_image': 'true'}).data), 1)
            self.client.force_authenticate(self.other)
            self.assertEqual(self.client.get(url + 'image/').status_code, 404)
            self.client.force_authenticate(self.owner)
            note.refresh_from_db()
            note.image.storage.delete(note.image.name)
            self.assertEqual(self.client.get(url + 'image/').status_code, 404)
            self.assertEqual(self.client.patch(url, {'image': None}, format='json').status_code, 200)
            self.assertEqual(self.client.get('/api/v1/note/', {'has_image': 'true'}).data, [])
