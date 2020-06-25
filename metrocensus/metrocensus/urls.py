from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("", lambda r: HttpResponse()),
    path("admin-panel/", include(("metrocensus.admin.urls", "admin"), namespace="admin")),
    
]