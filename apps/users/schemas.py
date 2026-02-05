from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.users.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    TokenResponseSerializer,
)


def register_user_schema():
    return extend_schema(
        tags=["Auth"],
        summary="Register user",
        description="Register a new user with email and password.",
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(description="User registered successfully"),
            400: OpenApiResponse(description="Bad request"),
        },
    )

def login_user_schema():
    return extend_schema(
        tags=["Auth"],
        summary="Login user",
        description="Login user with email and password.",
        request=UserLoginSerializer,
        responses={
            200: TokenResponseSerializer,
            400: OpenApiResponse(description="Invalid credentials"),
        }
    )

def display_profile_schema():
    return extend_schema(
        tags=["User"],
        summary="User profile",
        description="Display user profile information.",
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        }
    )
