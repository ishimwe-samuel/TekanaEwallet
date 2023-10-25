from rest_framework.urls import path
from api.auth.views import Login, RefreshToken, VerifyToken

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('refresh/', RefreshToken.as_view(), name='refresh'),
    path('verify/', VerifyToken.as_view(), name='verify')
]
