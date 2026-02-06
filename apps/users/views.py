import logging
from drf_spectacular.utils import extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.schemas import register_user_schema, login_user_schema, display_profile_schema
from apps.users.services import login_with_tokens, get_client_ip
from apps.users.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)

logger = logging.getLogger("auth")


@extend_schema_view(
    post=register_user_schema,
)
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Resister a new user with email and password.
        Return a success message.
        """
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(
            f"User registered | user_id={user.id} | ip={request.META.get('REMOTE_ADDR')}"
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


@extend_schema_view(
    post=login_user_schema,
)
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Authenticate user with email and password.
        Return access & refresh tokens via login_with_tokens()
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        ip = get_client_ip(request)
        data = login_with_tokens(email, password, ip=ip)
        logger.info(
            f"User login | email={email} | ip={ip}"
        )
        return Response(data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=display_profile_schema,
)
class UserProfileView(generics.RetrieveAPIView):
    """
    Display user profile details.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
