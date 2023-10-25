from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import viewsets
from users.models import User
from users.signals import user_account_created
from api.v1.users.serializers import UserCreateSerializer, UserSerializer, OTPSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action == "create_account":
            self.permission_classes = [AllowAny]
        if self.action == "list":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create_account":
            return UserCreateSerializer
        if self.action == "activate_account":
            return OTPSerializer
        return super().get_serializer_class()

    @action(["POST"], detail=False, url_path="create-account")
    def create_account(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_account_created.send(self, user=serializer.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(["POST"], detail=False, url_path="activate-account")
    def activate_account(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.otp
        user = otp.user
        user.active = True
        user.save()
        otp.is_active = False
        otp.save()
        return Response(status=status.HTTP_202_ACCEPTED)
