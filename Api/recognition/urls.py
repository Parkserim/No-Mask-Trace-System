from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("recognition/", views.RecognitionListCreateAPI.as_view()),
    path("recognition/<int:pk>", views.RecognitionViewAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
