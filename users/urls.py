from .api_views import UserRecordView,UserIDView,SetPasswordViewSet

from rest_framework.routers import DefaultRouter
from .template_views import login_view, register_user,logout,user_page,notification ,mine_users
from django.urls import path , include


router = DefaultRouter()

# router.register(r'user', views.UserViewSet)
router.register(r'reset_password', SetPasswordViewSet)
# router.register(r'account', views.AccountViewSet)


app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserRecordView.as_view(), name='users'),
    path('user_detail=<user_name>', UserIDView.as_view(), name='users'),

   # Django  template
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('logout/', logout, name="logout"),
    path('user_page/', user_page, name="user_page"),
    path('notification', notification, name="notification"),

    path('mine_users/', mine_users, name="mine_users"),
]




