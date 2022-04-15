from django.http import JsonResponse
import uuid
import time
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from job.models import Job
from job.tasks import runjob


@csrf_exempt
@require_http_methods(["POST"])
def job(request):
    id = uuid.uuid4()

    try:
        j = Job.create(
            job_uuid = id,
            status = "created",
            **request.POST.dict()
        )
    except Exception as e:
        return JsonResponse({"error": f"unable to save inputs: {e.args}"})

    validated_data = model_to_dict(j)

    try:
        print("id: ", id)
        runjob.s(id).apply_async()
    except Exception as e:
        return JsonResponse({"error": e.args})

    return JsonResponse({"job_uuid": id})


@csrf_exempt
@require_http_methods(["GET"])
def result(request):
    try: 
        job_uuid = request.GET["job_uuid"]
    except Exception as e:
        # print(e)
        return JsonResponse({"error": "must provide job_uuid"}, status=400)

    try:
        uuid.UUID(job_uuid)  # raises ValueError if not valid uuid
    except:
        return JsonResponse({"error": "invalid job_uuid format"}, status=400)

    try:
        j = Job.objects.get(job_uuid=job_uuid)
    except:
        return JsonResponse({"error": f"job_uuid {job_uuid} not found"}, status=400)
    
    return JsonResponse(model_to_dict(j), status=200)
