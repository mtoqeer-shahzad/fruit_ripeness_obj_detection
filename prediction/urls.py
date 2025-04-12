from django.urls import path

from myproject import settings
from . import views
from .views import DeletePredictionView, ImageClassificationView,TotalPredictionsCountView,SaveRecordView,DeleteAllPredictionsView, UserPredictionsView

urlpatterns = [
    path('upload-image/', ImageClassificationView.as_view(), name='ImageClassificationView'),
    path('save-record/', SaveRecordView.as_view(), name='save-record'),
    path('delete-prediction/<int:pk>/', DeletePredictionView.as_view(), name='delete-prediction'),
    path('delete-prediction/', DeleteAllPredictionsView.as_view(), name='delete-prediction'),
    path('predictions/total-count/', TotalPredictionsCountView.as_view(), name='total-predictions-count'),
     path('predictions/<str:username>/', UserPredictionsView.as_view(), name='user-predictions'),
]
