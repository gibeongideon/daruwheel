# from django.conf.urls import url
from spinchannel.views import log_in,sign_up,user_list,log_out,daru_spin,register_user,spin#,history, user_list
# from django.conf.urls.static import static
# from django.conf import settings
from django.urls import path
# from .views import login_view, register_user
from django.contrib.auth.views import LogoutView



app_name = 'spinchannel'

urlpatterns = [
    path('login/', log_in, name="log_in"),
    path('sign_up/', sign_up, name="sign_up"),
    path('register/', register_user, name="register_user"),
    path('log_out/', log_out, name="log_out"),
    path('', daru_spin, name="daru_spin"),
    path('spin/', spin, name='spin'), #
    path('user_list/', user_list, name="user_list"),
    path("logout/", LogoutView.as_view(), name="logout")

]


# urlpatterns = [
#     path('login/', login_view, name="login"),
#     path('register/', register_user, name="register"),
#     path("logout/", LogoutView.as_view(), name="logout")
# ]