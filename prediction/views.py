import numpy as np
import tensorflow as tf
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageUploadSerializer, PredictionResultSerializer
from .models import PredictionResult
from PIL import Image
import os
import logging

# Logger setup
logger = logging.getLogger(__name__)

# Load the trained model
MODEL_PATH = os.path.join(os.getcwd(), 'prediction', 'public', 'Image_classify.h5')
LABELS_PATH = os.path.join(os.getcwd(), 'prediction', 'public', 'labels.txt')

try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# Load class labels with a fallback option
class_labels = ["Apple", "Banana", "Grape", "Orange"]  # Default labels
try:
    if os.path.exists(LABELS_PATH):
        with open(LABELS_PATH, 'r') as f:
            class_labels = [line.strip() for line in f.readlines()]
    else:
        logger.warning(f"Labels file not found at {LABELS_PATH}, using default labels")
except Exception as e:
    logger.error(f"Error reading labels file: {e}, using default labels")


class ImageClassificationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            # image_path = default_storage.save(image.name, image)  # Save the image to default storage
            image_path = default_storage.save(f"images/{image.name}", image)
            try:
                # Load and preprocess image
                img = Image.open(image).convert("RGB")
                img = img.resize((256, 256))  # Resize to the input size expected by the model
                img_array = np.array(img) / 255.0  # Normalize the image
                img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

                if model is None:
                    return Response({"error": "Model not loaded"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Predict category
                predictions = model.predict(img_array)
                predicted_class = np.argmax(predictions)
                confidence = float(np.max(predictions) * 10)  # Convert to percentage confidence

                # Map to category and stage
                category_name = class_labels[predicted_class] if predicted_class < len(class_labels) else "Unknown"
                stage = "Overripe" if category_name == "Overripe" else "Ripe" if category_name == "Ripe" else "Unripe"

                # Save result in database
                prediction_result = PredictionResult.objects.create(
                    image=image_path,
                    category_name=category_name,
                    stage=stage,
                    confidence=confidence
                )

                response_data = PredictionResultSerializer(prediction_result).data
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error processing image: {e}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        predictions = PredictionResult.objects.all()
        serializer = PredictionResultSerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaveRecordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PredictionResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePredictionView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            # Get the prediction object by primary key (id)
            prediction = PredictionResult.objects.get(pk=pk)

            # Delete the prediction record from the database
            prediction.delete()

            # Return a success response
            return Response({"message": "Prediction deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except PredictionResult.DoesNotExist:
            raise NotFound("Prediction record not found.")
#==================================all prediction deleted=============================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PredictionResult

class DeleteAllPredictionsView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            # Delete all prediction records
            PredictionResult.objects.all().delete()

            # Return a success response
            return Response({"message": "All predictions deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#=============================TotalPredictionsCount=======================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PredictionResult

class TotalPredictionsCountView(APIView):
    def get(self, request):
        total_predictions = PredictionResult.objects.count()
        return Response({"total_predictions": total_predictions}, status=status.HTTP_200_OK)
#==================check image prediction with username
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PredictionResult
from django.contrib.auth.models import User

class UserPredictionsView(APIView):
    def get(self, request, username):
        try:
            # Fetch the user based on the username
            user = User.objects.get(username=username)
            
            # Fetch all predictions for the given user
            predictions = PredictionResult.objects.filter(user=user)
            
            # If no predictions exist, return an empty list
            if not predictions.exists():
                return Response({"message": "No predictions found for this user."}, status=status.HTTP_404_NOT_FOUND)

            # Prepare a list of predictions to return
            predictions_data = []
            for prediction in predictions:
                predictions_data.append({
                    "id": prediction.id,
                    "result": prediction.result,  # Assuming result stores the prediction result
                    "timestamp": prediction.timestamp,  # Assuming timestamp is when the prediction was made
                })

            return Response({"predictions": predictions_data}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)