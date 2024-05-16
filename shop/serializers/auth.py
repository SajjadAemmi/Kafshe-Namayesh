from rest_framework.serializers import CharField, BooleanField
from shop.conf import app_settings


class LoginSerializer:
    stay_logged_in = BooleanField(required=False)

