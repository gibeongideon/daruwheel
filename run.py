from time import sleep
from users.models import MarketInstance
 
def control():
    sleep(5)
    MarketInstance.objects.create()
    
while True:
    control()
