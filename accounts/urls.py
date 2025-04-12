from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserListView, UserDetailView, update_user, delete_user

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/update/<int:user_id>/', update_user, name='user-update'),  # FIXED UPDATE URL
    path('users/delete/<int:user_id>/', delete_user, name='user-delete'),
]
