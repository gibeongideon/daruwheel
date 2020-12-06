from .views import UserRecordView,UserIDView

from rest_framework.routers import DefaultRouter

from . import views
from django.urls import path , include


router = DefaultRouter()

# router.register(r'user', views.UserViewSet)
router.register(r'reset_password', views.SetPasswordViewSet)
# router.register(r'account', views.AccountViewSet)


app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserRecordView.as_view(), name='users'),
    path('user_detail=<user_name>', UserIDView.as_view(), name='users'),
]



