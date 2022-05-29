
from rest_framework.test import APITestCase
from movies.tasks import send_notification_email, upload_popular_movies


class TestAddTask(APITestCase):
    def setUp(self):
        data = [
            {
                'id': 1,
                'movie': {'title': 'Test'},
                'user': {'email': 'test'}
            }
        ]
        self.task = send_notification_email.delay(data)
        self.results = self.task.get()

    def test_task_state_send_email(self):
        self.assertEqual(self.task.state, 'SUCCESS')

    def test_result_send_email(self):
        self.assertEqual(self.results, 'Emails were send')

    def test_upload_popular_movies(self):
        results = upload_popular_movies.apply()
        self.assertEqual(results.get(), True)
        self.assertEqual(results.state, 'SUCCESS')
