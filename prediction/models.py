
from django.db import models

class PredictionResult(models.Model):
    image = models.ImageField(upload_to='uploads/')
    category_name = models.CharField(max_length=50)
    stage = models.CharField(max_length=50)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
