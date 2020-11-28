from recognition.models import Recognition
from rest_framework import serializers


class RecognitionSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recognition
        fields = ("pk", "encodeLst", "description", "created_at", "image")

