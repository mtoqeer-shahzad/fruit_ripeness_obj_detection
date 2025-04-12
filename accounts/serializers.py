from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

from rest_framework import serializers
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate using email as username
        user = authenticate(username=email, password=password)

        if user:
            if not user.is_active:
                raise serializers.ValidationError("User is not active.")
            return user
        raise serializers.ValidationError("Incorrect credentials.")

# from rest_framework import serializers
# from .models import CustomUser
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'is_active', 'date_joined']

# this is for forgot password Api

from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from .models import CustomUser

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct reset URL
        reset_url = f"http://yourfrontend.com/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_url}",
            "noreply@yourdomain.com",
            [user.email],
            fail_silently=False,
        )

        return value

# this is my Reset Password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser

# class ResetPasswordSerializer(serializers.Serializer):
#     uidb64 = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(write_only=True, min_length=8)
#
#     def validate(self, data):
#         try:
#             uid = urlsafe_base64_decode(data["uidb64"]).decode()
#             user = CustomUser.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#             raise serializers.ValidationError("Invalid user.")
#
#         if not default_token_generator.check_token(user, data["token"]):
#             raise serializers.ValidationError("Invalid or expired reset token.")
#
#         user.set_password(data["new_password"])
#         user.save()
#         return data

from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_active', 'date_joined','password']
