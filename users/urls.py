# om django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path, include


router = DefaultRouter()

router.register(r'user', views.UserViewSet)
router.register(r'users', views.CustomUserViewSet)
router.register(r'account', views.AccountViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('rest-auth/', include('rest_auth.urls')),
]