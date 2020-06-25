from metrocensus.admin.views import UserCreationView
from django.urls import path

urlpatterns = [
    path("create-user/", UserCreationView.as_view(), name="user_creation"),
]
