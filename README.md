# pyjulapi
A demonstration of how to create a Python API that also calls Julia code.

## Quick start
1. Install docker
2. Run `docker-compose up` from this repo's top directory
3. Create a job with `curl -X POST "localhost:8000/job"`, which will return `{"job_uuid": "57ca5074-05cc-4a60-830a-9af9a1b8641e"}`
4. Copy the `job_uuid` and pass it to the result endpoint with `curl -X GET "localhost:8000/result?job_uuid=57ca5074-05cc-4a60-830a-9af9a1b8641e"`

## Summary
- The Python Django package is used to create the external API (exposes port 8000). 
- Within Django we use Postgres to store the data.
- Within Django we use Celery to manage asynchronous tasks, specifically a python task called `runjob` is kicked off in the `job` view
- (Redis is used as the task queue for Celery)
- The `runjob` task calls an internal Julia API to further process the job.
- Results are updated in the Postgres database, which the user can receive via the `result` endpoint.