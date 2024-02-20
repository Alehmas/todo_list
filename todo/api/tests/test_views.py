from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.models import Task, User


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='auth', first_name='auth', password='qazxsw321'
        )
        cls.user2 = User.objects.create_user(
            username='auth2', first_name='auth2', password='321qazxsw'
        )
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

    def test_get_tasks_list_return_correct_context(self):
        """GET request /api/tasks/ returns correct data."""
        response = self.authorized_client.get('/api/tasks/')
        tasks = response.json()['results']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].get('title'), TaskURLTests.task.title)
        self.assertEqual(tasks[0].get('description'), TaskURLTests.task.description)
        self.assertEqual(tasks[0].get('status'), TaskURLTests.task.status)
        self.assertEqual(tasks[0].get('user_id'), TaskURLTests.task.user_id.id)

    def test_get_task_return_correct_context(self):
        """GET request /api/tasks/{id}/ returns correct data."""
        response = self.authorized_client.get(f'/api/tasks/{TaskURLTests.task.id}/')
        task_db = response.json()
        self.assertEqual(task_db.get('id'), TaskURLTests.task.id)
        self.assertEqual(task_db.get('title'), TaskURLTests.task.title)
        self.assertEqual(task_db.get('description'), TaskURLTests.task.description)
        self.assertEqual(task_db.get('status'), TaskURLTests.task.status)
        self.assertEqual(task_db.get('user_id'), TaskURLTests.task.user_id.id)

    def test_get_my_task_return_correct_context(self):
        """GET request /api/tasks/my/ returns correct data."""
        url = '/api/tasks/'
        self.authorized_client2.post(url, TaskURLTests.full_data)
        response_root = self.authorized_client2.get(url)
        response = self.authorized_client2.get('/api/tasks/my/')
        tasks = response.json()['results']
        self.assertEqual(len(response_root.json()['results']), 2)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].get('title'), TaskURLTests.full_data.get('title'))
        self.assertEqual(tasks[0].get('description'), TaskURLTests.full_data.get('description'))
        self.assertEqual(tasks[0].get('status'), TaskURLTests.full_data.get('status'))
        self.assertEqual(tasks[0].get('user_id'), TaskURLTests.user2.id)

    def test_post_tasks_return_correct_context(self):
        """POST request /api/tasks/ returns correct data."""
        response = self.authorized_client.post('/api/tasks/', TaskURLTests.full_data)
        new_task = response.json()
        self.assertEqual(new_task.get('title'), TaskURLTests.full_data.get('title'))
        self.assertEqual(new_task.get('description'), TaskURLTests.full_data.get('description'))
        self.assertEqual(new_task.get('status'), TaskURLTests.full_data.get('status'))
        self.assertEqual(new_task.get('user_id'), TaskURLTests.user.id)

    def test_post_tasks_add_taks_to_db(self):
        """POST request /api/tasks/ adds new task to database and correct data."""
        self.authorized_client.post('/api/tasks/', TaskURLTests.full_data)
        response = self.authorized_client.get('/api/tasks/')
        tasks = response.json()['results']
        self.assertEqual(len(tasks), 2)
        # In model order is from newest that means a new task is first in request
        self.assertEqual(tasks[0].get('title'), TaskURLTests.full_data.get('title'))
        self.assertEqual(tasks[0].get('description'), TaskURLTests.full_data.get('description'))
        self.assertEqual(tasks[0].get('status'), TaskURLTests.full_data.get('status'))
        self.assertEqual(tasks[0].get('user_id'), TaskURLTests.user.id)

    def test_put_tasks_return_correct_context(self):
        """PUT request /api/tasks/{id}/ returns correct data."""
        response = self.authorized_client.put(
            f'/api/tasks/{TaskURLTests.task.id}/', TaskURLTests.full_data)
        task_db = response.json()
        self.assertEqual(task_db.get('title'), TaskURLTests.full_data.get('title'))
        self.assertEqual(task_db.get('description'), TaskURLTests.full_data.get('description'))
        self.assertEqual(task_db.get('status'), TaskURLTests.full_data.get('status'))
        self.assertEqual(task_db.get('user_id'), TaskURLTests.user.id)

    def test_put_task_change_in_db(self):
        """PUT request /api/tasks/{id}/ changes task in db and correct data."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        self.authorized_client.put(url, TaskURLTests.full_data)
        response = self.authorized_client.get(url)
        changed_task = response.json()
        self.assertEqual(changed_task.get('title'), TaskURLTests.full_data.get('title'))
        self.assertEqual(changed_task.get('description'), TaskURLTests.full_data.get('description'))
        self.assertEqual(changed_task.get('status'), TaskURLTests.full_data.get('status'))
        self.assertEqual(changed_task.get('user_id'), TaskURLTests.user.id)

    def test_patch_task_return_correct_context(self):
        """PATCH request /api/tasks/{id}/ returns correct data."""
        response = self.authorized_client.patch(
            f'/api/tasks/{TaskURLTests.task.id}/', TaskURLTests.part_data)
        task_db = response.json()
        self.assertEqual(task_db.get('title'), TaskURLTests.part_data.get('title'))
        self.assertEqual(task_db.get('description'), TaskURLTests.task.description)
        self.assertEqual(task_db.get('status'), TaskURLTests.task.status)
        self.assertEqual(task_db.get('user_id'), TaskURLTests.task.user_id.id)

    def test_patch_task_change_in_db(self):
        """PATCH request /api/tasks/{id}/ changes task in db and correct data."""
        url = f'/api/tasks/{TaskURLTests.task.id}/'
        self.authorized_client.patch(url, TaskURLTests.part_data)
        response = self.authorized_client.get(url)
        changed_task = response.json()
        self.assertEqual(changed_task.get('title'), TaskURLTests.part_data.get('title'))
        self.assertEqual(changed_task.get('description'), TaskURLTests.task.description)
        self.assertEqual(changed_task.get('status'), TaskURLTests.task.status)
        self.assertEqual(changed_task.get('user_id'), TaskURLTests.task.user_id.id)

    def test_patch_task_change_status_completed(self):
        """PATCH request /api/tasks/{id}/completed/ changes status in db and correct data."""
        self.authorized_client.patch(f'/api/tasks/{TaskURLTests.task.id}/completed/')
        response = self.authorized_client.get(f'/api/tasks/{TaskURLTests.task.id}/')
        completed_task = response.json()
        self.assertEqual(completed_task.get('title'), TaskURLTests.task.title)
        self.assertEqual(completed_task.get('description'), TaskURLTests.task.description)
        self.assertEqual(completed_task.get('status'), 'Completed')
        self.assertEqual(completed_task.get('user_id'), TaskURLTests.task.user_id.id)

    def test_delete_task_is_not_in_db(self):
        """DELETE request /api/tasks/{id}/ deletes task in db."""
        self.authorized_client.delete(f'/api/tasks/{TaskURLTests.task.id}/')
        response = self.authorized_client.get('/api/tasks/')
        self.assertEqual(len(response.json()['results']), 0)

    # Cheking filtration
    def test_filtration(self):
        """Request /api/tasks/, /api/tasks/my/ is filtered by status."""
        self.authorized_client.post(
            '/api/tasks/', {'title': 'Test Task2', 'status': 'Completed'})
        self.authorized_client.post(
            '/api/tasks/', {'title': 'Test Task2', 'status': 'In Progress'})
        api_names = {
            '/api/tasks/': 3,
            '/api/tasks/' + '?status=New': 1,
            '/api/tasks/' + '?status=Completed': 1,
            '/api/tasks/' + '?status=In Progress': 1,
            '/api/tasks/my/': 3,
            '/api/tasks/my/' + '?status=New': 1,
            '/api/tasks/my/' + '?status=Completed': 1,
            '/api/tasks/my/' + '?status=In Progress': 1,
        }
        for url_pattern, value in api_names.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(url_pattern)
                self.assertEqual(len(response.json()['results']), value)


# Checking the paginator
class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='auth', first_name='auth', password='qazxsw321'
        )
        number_task = 13
        for task_num in range(number_task):
            Task.objects.create(
                title=f'Title test task{str(task_num)}',
                user_id=cls.user
            )

    def setUp(self):
        self.authorized_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.authorized_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_paginator(self):
        """Number of tasks on pages 1 and 2 /api/tasks/ and /api/tasks/my."""
        api_names = {
            '/api/tasks/': 10,
            '/api/tasks/' + '?page=2': 3,
            '/api/tasks/my/': 10,
            '/api/tasks/my/' + '?page=2': 3
        }
        for url_pattern, value in api_names.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(url_pattern)
                self.assertEqual(len(response.json()['results']), value)
