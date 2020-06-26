from django.urls import path
from rest_framework import routers

from metrocensus.admin.views import CreateTokenView, UserViewSet

router = routers.SimpleRouter()
router.register(r"admin-panel/users", UserViewSet)

urlpatterns = [
    path("admin-panel/login/", CreateTokenView.as_view(), name="login"),
]

urlpatterns += router.urls
