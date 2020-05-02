from django.urls import include, re_path
from rest_framework import routers

router = routers.DefaultRouter()

url_patterns = [re_path("", include(router.urls))]
