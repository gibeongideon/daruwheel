
# from users.models import MarketInstance
from time import sleep

from users.models import MarketInstance

from 


def control():
    try:
        while True:
            MarketInstance.objects.create()
            sleep(10)

    except Exception as e:
        print('CONTROL',e)
        return e



# if '__name__' = '__main__':
#     control()
