from django.urls import path
from accounts.views import RegisterAPI, VerifyOTP, LoginAPI, LogoutAPI

# from unity_api.authentication_views import UserRegistrationAPIView, LoginAPIView


urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register-user"),
    path("verify/", VerifyOTP.as_view(), name="verify-user"),
    path("login/", LoginAPI.as_view(), name="login-user"),
    path("logout/", LogoutAPI.as_view(), name="logout-user"),
]
