from django.db import models

# Create your models here.

class Job(models.Model):
    job_uuid = models.UUIDField(unique=True)
    status = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj