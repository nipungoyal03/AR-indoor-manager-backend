from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "is_verified"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["id"] = instance.id
        data["is_verified"] = instance.is_verified
        return data


class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        model = User  # Assuming User is your model
        fields = ["email", "otp"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
