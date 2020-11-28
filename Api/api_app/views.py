from rest_framework import permissions, generics
from .serializers import (
    FileSerializer,
    DeviceSerializer,
    UserSerializer,
    LoginUserSerializer,
    CreateUserSerializer,
)
from .models import File, Device
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import mixins
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000


class FileViewAPI(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # permission_classes = [IsAuthenticated]


class FileFilter(filters.FilterSet):
    min_created_at = filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    max_created_at = filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = File
        fields = ("location", "sublocation")


class FileListCreateAPI(
    mixins.ListModelMixin, generics.GenericAPIView, mixins.CreateModelMixin,
):
    serializer_class = FileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter
    pagination_class = LargeResultsSetPagination
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = File.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DeviceViewAPI(APIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = DeviceSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = DeviceSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=204)


class DeviceListCreateAPI(
    mixins.ListModelMixin, generics.GenericAPIView,
):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = LargeResultsSetPagination
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Device.objects.all()
        return queryset

    def post(self, request):
        serializer = DeviceSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "registration success"}, status=201)
        return JsonResponse({"status": False})


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if (
            len(request.data["username"]) < 6
            or len(request.data["password"]) < 4
        ):
            body = {"message": "short field"}
            return Response(body)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
