from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from main.models import UploadedModel
from main.serializers import UploadedModelSerializer
from rest_framework.permissions import IsAuthenticated
import os


class UploadModelView(generics.CreateAPIView):
    queryset = UploadedModel.objects.all()
    serializer_class = UploadedModelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        max_file_size = 20 * 1024 * 1024
        allowed_file_formats = [".fbx"]

        if "model_file" in request.data:
            uploaded_file = request.data["model_file"]

            if uploaded_file.size > max_file_size:
                return Response(
                    {"error": "File size exceeds the allowed limit of 20 MB."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            file_name, file_extension = os.path.splitext(uploaded_file.name)
            if file_extension.lower() not in allowed_file_formats:
                return Response(
                    {"error": "Invalid file format. Only .fbx files are allowed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        serializer.save()

        return Response(
            {"id": serializer.instance.id, "message": "File uploaded successfully."},
            status=status.HTTP_201_CREATED,
        )


class GenerateUnityPackageView(generics.RetrieveAPIView):
    queryset = UploadedModel.objects.all()
    serializer_class = UploadedModelSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        model_file_path = instance.model_file.path

        # Create Unity package
        unity_package_path = self.create_unity_package(model_file_path)

        if unity_package_path:
            # Send the Unity package as a downloadable response
            return self.download_unity_package(unity_package_path)
        else:
            return Response(
                {"error": "Failed to generate Unity package"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
