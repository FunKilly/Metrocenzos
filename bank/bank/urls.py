from django.urls import path
from rest_framework import routers

from accounts.views import CitizenViewSet

router = routers.SimpleRouter()
router.register(r"api/citizens", CitizenViewSet)

urlpatterns = []
urlpatterns += router.urls