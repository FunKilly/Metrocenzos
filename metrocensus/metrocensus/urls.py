from django.urls import path
from rest_framework import routers

from admin.views import CitizenViewSet, CreateTokenView, UserViewSet

router = routers.SimpleRouter()
router.register(r"admin-panel/users", UserViewSet)
router.register(r"admin-panel/citizens", CitizenViewSet)

urlpatterns = [
    path("admin-panel/login", CreateTokenView.as_view(), name="login"),
]

urlpatterns += router.urls
