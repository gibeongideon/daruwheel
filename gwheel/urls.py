# om django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path, include


router = DefaultRouter()

router.register(r'market', views.MarketInstanceViewSet)
router.register(r'stake', views.StakeViewSet)

app_name = 'gwheel'

urlpatterns = [
    path('', include(router.urls)),
    # path('user/', UserRecordView.as_view(), name='users'),
    # path('user_trans/_start=<int:start>&_limit=<int:limit>/_user_id=<int:pk>', views.TransactionView.as_view()),
    #path('rest-auth/', include('rest_auth.urls')),
]


