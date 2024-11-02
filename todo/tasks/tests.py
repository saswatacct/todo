from django.contrib.auth import get_user_model
from django.test import TestCase

from todo.tasks.models import Task

User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testpassword",
        )

        self.project = self.user.projects.create(name="Test Project")

        # Create 3 tasks
        for i in range(1, 4):
            self.project.tasks.create(
                description=f"Test Task {i}",
            )


class TestTaskModel(BaseTest):
    def assertPriority(self, project_task: Task, priority: int):
        self.assertEqual(project_task.priority, priority)

        # Check the priority of the tasks in the project
        tasks = self.project.tasks.all()
        for i, task in enumerate(tasks):
            self.assertEqual(task.priority, i + 1)

            if task == project_task:
                self.assertEqual(task.priority, priority)

    def test_task_priority(self):
        task = self.project.tasks.create(
            description="Test Task 4",
        )

        self.assertPriority(task, 4)

        task.set_priority(1)

        self.assertPriority(task, 1)

        task.set_priority(3)

        self.assertPriority(task, 3)

        task.set_priority(1)

        self.assertPriority(task, 1)

        task.set_priority(4)

        self.assertPriority(task, 4)
