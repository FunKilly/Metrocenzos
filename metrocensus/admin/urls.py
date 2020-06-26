from metrocensus.admin.views import UserCreationView, CreateTokenView
from django.urls import path

urlpatterns = [
    path("create-user/", UserCreationView.as_view(), name="user_creation"),
    path("login/", CreateTokenView.as_view(), name="login"),
]
