from rest_framework.routers import DefaultRouter
from api.v1.accounts.views import AccountsViewSet
router= DefaultRouter()
router.register('account',AccountsViewSet)
urlpatterns = router.urls
