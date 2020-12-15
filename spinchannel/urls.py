from spinchannel.views import daru_spin
from django.urls import path


app_name = 'spinchannel'

urlpatterns = [
    path('', daru_spin, name="daru_spin"),
 

]
