from django.test import TestCase
"""
command line testing:

python manage.py shell
from django.test.utils import setup_test_environment
setup_test_environment()
from django.test import Client
client = Client()
"""


class JobViewTests(TestCase):

    def test_result_endpoint(self):
        fake_id = "4c141fdb-9e18-4f16-a093-09e79956c455"
        data = {
            "no_id": fake_id
        }
        response = self.client.get('/result', format='json', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("must provide job_uuid" in response.json()["error"])

        data = {
            "job_uuid": "1"
        }
        response = self.client.get('/result', format='json', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("invalid" in response.json()["error"])

        data = {
            "job_uuid": fake_id
        }
        response = self.client.get('/result', format='json', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("not found" in response.json()["error"])

    def test_job_endpoint(self):
        response = self.client.post('/job', format='json', data={})
        job_uuid = response.json()["job_uuid"]
        data = {
            "job_uuid": job_uuid
        }
        response = self.client.get('/result', format='json', data=data)
        j = response.json()
        self.assertTrue(j["status"] == "created")
