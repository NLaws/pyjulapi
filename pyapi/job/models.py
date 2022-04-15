from django.db import models
from django.utils import timezone
# Create your models here.

class Job(models.Model):
    job_uuid = models.UUIDField(unique=True)
    status = models.TextField(blank=False)
    created = models.DateTimeField(default=timezone.now)
    valid_input_int = models.IntegerField(default=1)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj