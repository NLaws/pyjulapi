import time
from job.models import Job
from celery import shared_task
import requests
import os


@shared_task()
def runjob(id):
    time.sleep(1)  # give the database time to update
    j = Job.objects.get(job_uuid=id)
    # 1. do python task
    j.status = "running python task..."
    j.save()
    time.sleep(10)  # simulate some think time

    d = {"output": j.valid_input_int * 2}
    j.status = "python task complete. running julia task ..."
    j.result=d
    j.save()

    # 2. do julia task
    julia_host = os.environ.get('JULIA_HOST', "julia")
    response = requests.post("http://" + julia_host + ":8081/job/", json=d)
    time.sleep(8)  # simulate some think time
    d = response.json()

    # 3. save results
    j.result = d
    j.status = "complete"
    j.save()
