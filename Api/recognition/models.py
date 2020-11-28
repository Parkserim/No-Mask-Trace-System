from django.db import models
import json
from django.utils import timezone


class Recognition(models.Model):
    encodeLst = models.TextField(null=True, blank=True,)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    description = models.TextField(null=True, blank=True)

    def set_encodeLst(self, x):
        self.encodeLst = json.dumps(x)

    def get_encodeLst(self):
        return json.loads(self.encodeLst)

    def date_upload_to(instance, filename):
        date = timezone.now().strftime("%Y/%m/%d")
        return f"{date}/{filename}"

    image = models.ImageField(
        default="media/default_image.jpg", upload_to=date_upload_to, null=True
    )

