

from django.urls import path, re_path
from core import views

app_name = 'core'

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
    path('icons', views.icons, name='icons'),
    path('maps', views.maps, name='maps'),
    path('topo', views.topo, name='topo'),

]
