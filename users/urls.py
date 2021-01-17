from .api_views import UserRecordView
from rest_framework.routers import DefaultRouter

from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import template_views as views


router = DefaultRouter()

app_name = 'users'

urlpatterns = [
    # path('', include(router.urls)),
    path('user/', UserRecordView.as_view(), name='users'),
#     path('user_detail=<user_name>', UserIDView.as_view(), name='users'),

#    # Django  template
    # path('login', views.login_view, name="login"),
#     path('register/', views.register_user, name="register"),
#     path('logout/', views.logout, name="logout"),
    path('user_page', views.user_page, name="user_page"),
    path('notification', views.notification, name="notification"),

    path('mine_users', views.mine_users, name="mine_users"),

#     path('', views.index, name='index'),
#     path('roulette', views.roulette, name='roulette'),
#     path('deposit', views.deposit, name='deposit'),
#     path('withdraw', views.withdraw, name='withdraw'),
#     path('seed', views.seed, name='seed'),
#     path('provably', views.provably, name='provably'),
#     path('shoutbox', views.shoutbox, name='shoutbox'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
#     re_path(r'^password_reset/$', auth_views.password_reset,
#             name='password_reset'),
#     re_path(r'^password_reset/done/$', auth_views.password_reset_done,
#             name='password_reset_done'),
#     re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
#             '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#             auth_views.password_reset_confirm, name='password_reset_confirm'),
#     re_path(r'^reset/done/$', auth_views.password_reset_complete,
#             name='password_reset_complete'),
#     path("checkout", views.deposit_checkout, name="deposit_checkout"),
#     path("wamp_init", views.wamp_init),
]


