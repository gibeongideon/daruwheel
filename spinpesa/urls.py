"""spinpesa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from mpesa.urls import mpesa_urls  #  No module named 'requests

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Daricash Admin'
# admin.site.index_title = ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls',namespace='users')),
    path('account/', include('account.urls',namespace='accounts')),
    path('gwheel/', include('gwheel.urls',namespace='gwheels')),
    path('spin/', include('spinchannel.urls',namespace='spinchannel')),
    path('chat/', include('chat.urls',namespace='chat')),
    path('mpesa/', include(mpesa_urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    
] + static(settings.STATIC_URL)