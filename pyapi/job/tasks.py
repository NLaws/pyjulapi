import time
from job.models import Job
from celery import shared_task


@shared_task()
def runjob(id):
    time.sleep(1)  # give the database time to update
    j = Job.objects.get(job_uuid=id)
    # 1. do python task
    j.status="running python task..."
    j.save()
    time.sleep(10)

    d = {"output": j.valid_input_int * 2}
    j.status="python task complete. running julia task ..."
    j.result=d
    j.save()

    # 2. do julia task
    time.sleep(10)
    d = {"output": j.valid_input_int * 3}
    j.result=d
    j.status="complete"
    j.save()

    # 3. save results