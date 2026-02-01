import logging
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.services import login_with_tokens, get_client_ip

from apps.users.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)

logger = logging.getLogger("auth")

@extend_schema(
    request=UserRegisterSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
            },
        },
    },
    tags=["User"],
)
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(
            f"User registered | user_id={user.id} | ip={request.META.get('REMOTE_ADDR')}"
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["User"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["email", "password"],
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
                "refresh": {"type": "string"},
            }
        }
    },
)
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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


@extend_schema(tags=["User"])
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
