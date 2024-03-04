from django.db import models


class UploadedModel(models.Model):
    model_file = models.FileField(upload_to="uploaded_models/")
