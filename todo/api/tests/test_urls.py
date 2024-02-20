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
        cls.user2 = User.objects.create_user(
            username='auth2', first_name='auth2')
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
        self.authorized_client2 = APIClient()
        refresh2 = RefreshToken.for_user(self.user2)
        self.authorized_client2.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh2.access_token}')

    def test_get_tasks_anonymous(self):
        """GET request /api/tasks/, /api/tasks/my/, /api/tasks/{id}/ is not available to anonymous."""
        task_url_names = {
            '/api/tasks/': status.HTTP_401_UNAUTHORIZED,
            '/api/tasks/my/': status.HTTP_401_UNAUTHORIZED,
            f'/api/tasks/{TaskURLTests.task.id}/': status.HTTP_401_UNAUTHORIZED,
        }
        for url, status_code in task_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEquals(response.status_code, status_code)

    def test_post_tasks_anonymous(self):
        """POST request /api/tasks/ is not available to anonymous."""
        url = '/api/tasks/'
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_tasks_anonymous(self):
        """PUT request /api/tasks/{id}/ is not available to anonymous."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.guest_client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_del_tasks_anonymous(self):
        """DELETE request /api/tasks/{id}/ is not available to anonymous."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_tasks_anonymous(self):
        """PATCH request /api/tasks/{id}/, /api/tasks/{id}/completed is not available to anonymous."""
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
                         """Request with full data returns status 201.""")
        response = self.authorized_client.post(url, data=TaskURLTests.part_data)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         """Request with incomplete data returns status 201.""")
        response = self.authorized_client.post(url, data=TaskURLTests.wrong_data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         """Request without required field title returns status 400.""")

    def test_put_tasks_autor(self):
        """PUT request /api/tasks/{id}/ is available to author."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client.put(url, TaskURLTests.full_data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         """Request with full data returns status 200.""")
        response = self.authorized_client.put(url, TaskURLTests.wrong_data)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         """Request with wrong data returns status 400.""")

    def test_put_tasks_non_author(self):
        """PUT request /api/tasks/{id}/ is not available for other author."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client2.put(url, TaskURLTests.full_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_del_tasks_autorized(self):
        """DELETE request /api/tasks/{id}/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_del_tasks_non_author(self):
        """DELETE request /api/tasks/{id}/ is not available for other author."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_task_autorized(self):
        """PATCH request /api/tasks/{id}/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client.patch(url, TaskURLTests.part_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task_non_author(self):
        """PATCH request /api/tasks/{id}/ is not available for other author."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        response = self.authorized_client2.patch(url, TaskURLTests.part_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_task_completed_autorized(self):
        """PATCH request /api/tasks/{id}/completed/ is available to authorized."""
        url = f'/api/tasks/{TaskURLTests.task.id}/completed/'
        response = self.authorized_client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task_double_completed_to_author(self):
        """PATCH double request /api/tasks/{id}/completed/ is not available."""
        url = f'/api/tasks/{TaskURLTests.task.id}/completed/'
        response = self.authorized_client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.authorized_client.patch(url)
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)

    def test_patch_task_completed_to_non_author(self):
        """PATCH request /api/tasks/{id}/completed/ is not available for other author."""
        url = f'/api/tasks/{TaskURLTests.task.id}/completed/'
        response = self.authorized_client2.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unexisting_page(self):
        """The unexisting_page/ page will return status 404."""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
