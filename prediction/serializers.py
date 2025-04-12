# # from rest_framework import serializers
# # #
# # # class ImageUploadSerializer(serializers.Serializer):
# # #     image = serializers.ImageField()
# # from rest_framework import serializers
# # from .models import PredictionResult

# # class ImageUploadSerializer(serializers.Serializer):
# #     image = serializers.ImageField()

# # class PredictionResultSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PredictionResult
# #         fields = '__all__'
# # # class PredictionResultSerializer(serializers.ModelSerializer):
# # #     image_url = serializers.SerializerMethodField()

# # #     class Meta:
# # #         model = PredictionResult
# # #         fields = '__all__'  # Keeps all fields

# # #     def get_image_url(self, obj):
# # #         request = self.context.get('request')
# # #         if obj.image:
# # #             return request.build_absolute_uri(obj.image.url) if request else f"{settings.MEDIA_URL}{obj.image}"
# # #         return None


# from rest_framework import serializers
# from django.conf import settings
# from .models import PredictionResult

# class ImageUploadSerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()  # Add this field

#     class Meta:
#         model = PredictionResult
#         fields = ['id', 'image', 'category_name', 'stage', 'confidence', 'created_at', 'image_url']

#     def get_image_url(self, obj):
#         request = self.context.get('request')  # Get the request context
#         if obj.image:
#             return request.build_absolute_uri(obj.image.url)  # Build full URL
#         return None

from rest_framework import serializers
from django.conf import settings
from .models import PredictionResult

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()  # Only used for uploading images

class PredictionResultSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Get the full image URL

    class Meta:
        model = PredictionResult
        fields = ['id', 'image', 'category_name', 'stage', 'confidence', 'created_at', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request context if available
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)  # Full URL for API responses
            return f"{settings.MEDIA_URL}{obj.image}"  # Manual fallback for local usage
        return None
