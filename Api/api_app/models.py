from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class File(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)

    def date_upload_to(instance, filename):
        date = timezone.now().strftime("%Y/%m/%d")
        return f"{instance.location}/{instance.sublocation}/{date}/{filename}"

    image = models.ImageField(
        default="media/default_image.jpg", upload_to=date_upload_to,
    )
    location = models.CharField(
        max_length=50, default="Please Register Location", null=True
    )
    sublocation = models.CharField(
        max_length=50, default="Please Register Sub Location", null=True
    )


class Device(models.Model):
    location = models.CharField(
        max_length=50, default="Please Register Location", null=True
    )
    sublocation = models.CharField(
        max_length=50, default="Please Register Sub Location", null=True
    )

