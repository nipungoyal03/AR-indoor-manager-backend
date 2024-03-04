from django.urls import path
from main.views import UploadModelView

# from unity_api.authentication_views import UserRegistrationAPIView, LoginAPIView


urlpatterns = [
    path("upload/", UploadModelView.as_view(), name="upload-model"),
]
