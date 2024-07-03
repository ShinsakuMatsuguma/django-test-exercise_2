from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from todo.models import Task

# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1+2,3)

class TaskModelTestCase(TestCase):
    def test_create_task1(self):
        due=timezone.make_aware(datetime(2024,6,30,23,59,59))
        task=Task(title="task1",due_at=due)
        task.save()

        task=Task.objects.get(pk=task.pk)
        self.assertEqual(task.title,"task1")
        self.assertFalse(task.compleated)
        self.assertEqual(task.due_at,due)

    def test_create_task2(self):
        task=Task(title="task2")
        task.save()

        task=Task.objects.get(pk=task.pk)
        self.assertEqual(task.title,"task2")
        self.assertFalse(task.compleated)
        self.assertEqual(task.due_at,None)

    def test_is_overdue_future(self):
        due=timezone.make_aware(datetime(2024,6,30,23,59,59))
        current=timezone.make_aware(datetime(2024,6,30,0,0,0))
        task=Task(title="task1",due_at=due)
        task.save()
        self.assertFalse(task.is_overdue(current))

    def test_is_overdue_past(self):
        due=timezone.make_aware(datetime(2024,6,30,23,59,59))
        current=timezone.make_aware(datetime(2024,7,1,0,0,0))
        task=Task(title="task2",due_at=due)
        task.save()
        self.assertTrue(task.is_overdue(current))

    def test_is_overdue_none(self):
        current=timezone.make_aware(datetime(2024,7,1,0,0,0))
        task=Task(title="task3",due_at=None) 
        task.save()
        self.assertFalse(task.is_overdue(current))

class TodoViewTestCase(TestCase):
    def test_index_get(self):
        client = client()
        response = client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(len(response.context['tasks']), 0)
    def test_index_post(self):
        client = client()
        data = {
            'title': 'Task1',
            'due_at': '2024-06-30 23:59:59'
        }
        response = client.post('/', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(len(response.context['tasks']), 1)

    def test_index_get_order_due(self):
        task1 = Task(title='Task1',due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title='Task2',due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = client()
        response = client.get('/?order=due')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(response.context['tasks'][0].title, task2)
        self.assertEqual(response.context['tasks'][1].title, task1)