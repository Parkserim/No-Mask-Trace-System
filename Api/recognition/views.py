from rest_framework import permissions, generics
from .serializers import RecognitionSerializer
from .models import Recognition
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response


class RecognitionViewAPI(APIView):
    queryset = Recognition.objects.all()
    serializer_class = RecognitionSerializer

    def get_object(self, pk):
        try:
            return Recognition.objects.get(pk=pk)
        except Recognition.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = RecognitionSerializer(queryset)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = RecognitionSerializer(
            queryset, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class RecognitionListCreateAPI(
    mixins.ListModelMixin, generics.GenericAPIView, mixins.CreateModelMixin,
):
    queryset = Recognition.objects.all()
    serializer_class = RecognitionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Recognition.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

