from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("files/", views.FileListCreateAPI.as_view()),
    path("files/<int:pk>", views.FileViewAPI.as_view()),
    path("devices/", views.DeviceListCreateAPI.as_view()),
    path("devices/<int:pk>", views.DeviceViewAPI.as_view()),
    path("auth/login/", views.LoginAPI.as_view()),
    path("auth/user/", views.UserAPI.as_view()),
    # path("auth/register/", views.RegistrationAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
