from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import (
    UserSerializer,
    VerifyAccountSerializer,
    LoginSerializer,
)
from rest_framework import status
from accounts.email import send_otp_via_email
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class RegisterAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data["email"])
                return Response(
                    {
                        "message": "registration successful, please verify the OTP",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "message": "invalid credentials, maybe user already exist",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(e)
            return Response(
                {"message": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data["email"]
                otp = serializer.data["otp"]

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                            "message": "something went wrong. Invalid Email",
                            "data": "invalid email",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user = user.first()
                if user.otp != otp:
                    return Response(
                        {
                            "message": "something went wrong, Wrong OTP",
                            "data": "wrong otp",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user.is_verified = True
                user.save()

                return Response(
                    {"message": "account verified"}, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(e)
            return Response(
                {"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


# class LoginAPI(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             serializer = LoginSerializer(data=data)
#             if serializer.is_valid():
#                 email = serializer.validated_data["email"]
#                 password = serializer.validated_data["password"]
#                 print(email)
#                 print(password)
#                 # user=User.objects.get(email=email)
#                 user = authenticate(email=email, password=password)
#                 print(user)
#                 if user is None:
#                     return Response(
#                         {
#                             "message": "You are not registered",
#                             "data": {},
#                         },
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#                 if user.is_verified is False:
#                     return Response(
#                         {
#                             "message": "You are not verified",
#                             "data": {},
#                         },
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#
#                 refresh = RefreshToken.for_user(user)
#                 return Response(
#                     {
#                         "message": "login successful",
#                         "refresh": str(refresh),
#                         "access": str(refresh.access_token),
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#
#             return Response(
#                 {"message": "something went wrong", "data": serializer.errors},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         except Exception as e:
#             print(e)


# views.py


from django.contrib.auth.hashers import check_password


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]

                # Manually query the user object using email
                user = User.objects.filter(email=email).first()
                if user:
                    # DEBUG: Log email for comparison
#                     print("Stored Email:", user.email)
#                     print("Provided Email:", email)
# 
#                     # DEBUG: Log hashed password from the database
#                     print("Stored Hashed Password:", user.password)

                    # Authenticate user with provided password
                    if password == user.password:
                        # Ensure the user is verified before allowing login
                        if user.is_verified:
                            refresh = RefreshToken.for_user(user)
                            return Response(
                                {
                                    "message": "login successful",
                                    "refresh": str(refresh),
                                    "access": str(refresh.access_token),
                                },
                                status=status.HTTP_200_OK,
                            )
                        else:
                            return Response(
                                {"message": "You are not verified"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        # DEBUG: Log provided password for comparison
                        print("Provided Password:", password)

                        return Response(
                            {"message": "Invalid credentials"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"message": "User not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            return Response(
                {"message": "Something went wrong", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get("refresh_token")

            # If the refresh token is provided, blacklist it
            if refresh_token:
                RefreshToken(refresh_token).blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
