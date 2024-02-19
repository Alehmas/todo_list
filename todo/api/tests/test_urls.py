from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.models import Task, User


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='auth', first_name='auth')
        cls.task = Task.objects.create(
            title='Title test task',
            description='Test description',
            status='New',
            user_id=cls.user
        )
        cls.full_data = {'title': 'Test Task',
                         'description': 'This is a test task',
                         'status': 'New'}
        cls.part_data = {'title': 'Test Task'}
        cls.wrong_data = {'description': 'This is a test task'}

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.authorized_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_tasks_unauthenticated(self):
        """GET request /api/tasks/, /api/tasks/my/, /api/tasks/{id}/ is not available to unauthorized."""
        task_url_names = {
            '/api/tasks/': status.HTTP_401_UNAUTHORIZED,
            '/api/tasks/my/': status.HTTP_401_UNAUTHORIZED,
            f'/api/tasks/{TaskURLTests.task.id}/': status.HTTP_401_UNAUTHORIZED,
        }
        for url, status_code in task_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEquals(response.status_code, status_code)

    def test_post_tasks_unauthenticated(self):
        """POST request /api/tasks/ is not available to unauthorized."""
        url = '/api/tasks/'
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_tasks_unauthenticated(self):
        """PUT request /api/tasks/{id}/ is not available to unauthorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.guest_client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_del_tasks_unauthenticated(self):
        """DELETE request /api/tasks/{id}/ is not available to unauthorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_tasks_unauthenticated(self):
        """PATCH request /api/tasks/{id}/, /api/tasks/{id}/completed is not available to unauthorized."""
        task_url_names = {
            f'/api/tasks/{TaskURLTests.task.id}/': status.HTTP_401_UNAUTHORIZED,
            f'/api/tasks/{TaskURLTests.task.id}/completed/': status.HTTP_401_UNAUTHORIZED,
        }
        for url, status_code in task_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.patch(url)
                self.assertEquals(response.status_code, status_code)

    def test_get_tasks_autorized(self):
        """GET request /api/tasks/, /api/tasks/my/, /api/tasks/{id}/ is available to authorized."""
        task_url_names = {
            '/api/tasks/': status.HTTP_200_OK,
            '/api/tasks/my/': status.HTTP_200_OK,
            f'/api/tasks/{TaskURLTests.task.id}/': status.HTTP_200_OK,
        }
        for url, status_code in task_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEquals(response.status_code, status_code)

    def test_post_tasks_autorized(self):
        """POST request /api/tasks/ is available to authorized."""
        url = '/api/tasks/'
        response = self.authorized_client.post(url, data=TaskURLTests.full_data)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         """Request succeeds with full data.""")
        response = self.authorized_client.post(url, data=TaskURLTests.part_data)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         """Request succeeds with incomplete data.""")
        response = self.authorized_client.post(url, data=TaskURLTests.wrong_data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         """Request failed with wrong data.""")

    def test_put_tasks_autorized(self):
        """PUT request /api/tasks/{id}/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client.put(url, TaskURLTests.full_data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         """Request succeeds with full data.""")
        response = self.authorized_client.put(url, TaskURLTests.wrong_data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         """Request failed with wrong data.""")

    def test_del_tasks_autorized(self):
        """DELETE request /api/tasks/{id}/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_task_autorized(self):
        """PATCH request /api/tasks/{id}/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client.patch(url, TaskURLTests.part_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task_completed_autorized(self):
        """PATCH request /api/tasks/{id}/completed/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/completed/'
        response = self.authorized_client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task_completed_to_author(self):
        """PATCH request /api/tasks/{id}/completed/ is not available to non-author."""
        user2 = User.objects.create_user(username='auth2', first_name='auth2')
        authorized_client2 = APIClient()
        refresh2 = RefreshToken.for_user(user2)
        authorized_client2.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh2.access_token}')
        url = f'/api/tasks/{TaskURLTests.task.id}/completed/'
        response = authorized_client2.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
