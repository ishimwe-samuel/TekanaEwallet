from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView, AUTH_HEADER_TYPES, TokenError, InvalidToken
from api.auth.serializers import JWTTokenSerializer


class Login(TokenObtainPairView):
    """
    Login handler
    """
    serializer_class = JWTTokenSerializer
    permission_classes = ()
    authentication_classes = ()
    www_authenticate_realm = 'api'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshToken(TokenRefreshView):
    """
    Refresh token handler which extends TokenRefresh from simple jwt
    """
    pass


class VerifyToken(TokenVerifyView):
    """
    Verify token handler which extends TokenRefresh from simple jwt
    """
    pass
