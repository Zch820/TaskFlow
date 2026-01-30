import logging
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User

logger = logging.getLogger("auth")


def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')


def login_with_tokens(email, password, ip):
    user = User.objects.filter(email=email).first()

    if not user or not user.check_password(password):
        logger.warning(
            f"User login failed | email={email} | ip={ip}"
        )
        raise AuthenticationFailed("Invalid credentials")
    refresh = RefreshToken.for_user(user)

    data = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }
    return data
