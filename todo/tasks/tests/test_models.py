from django.test import TestCase

from tasks.models import Task, User


class TaskModelTest(TestCase):
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

    def test_verbose_name(self):
        """verbose_name in the fields matches what is expected."""
        task = TaskModelTest.task
        field_verboses = {
            'title': 'Title',
            'description': 'Description',
            'status': 'Status',
            'user_id': 'Author',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test_models_have_correct_object_names(self):
        """Check that models have __str__ working correctly."""
        user = TaskModelTest.user
        task = TaskModelTest.task
        field_str = {
            user: user.username,
            task: task.title,
        }
        for model, expected_value in field_str.items():
            with self.subTest(model=model):
                self.assertEqual(expected_value, str(model))
