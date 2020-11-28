from django.contrib import admin
from django.urls import path, include
import api_app.urls
import recognition.urls
from knox import views as knox_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(recognition.urls)),
    path("api/", include(api_app.urls)),
    path("api/auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
]
