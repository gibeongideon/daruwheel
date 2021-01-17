

from django.urls import path, re_path
from core import views
from spinchannel import views as spinview

app_name = 'core'

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', spinview.daru_spin, name='daru_spin'),
    path('icons', views.icons, name='icons'),
    path('maps', views.maps, name='maps'),
    path('topo', views.topo, name='topo'),
    path('support', views.support, name='support'),

]
