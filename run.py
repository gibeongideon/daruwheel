
from users.models import MarketInstance ,Result
from time import sleep
import random

def control():
    id = 152
    try:
        while True:
                MarketInstance.objects.create(id = id)
                sleep((8.5*60))
                print('getting  BACKGROUNG results')
                sleep(2)
                resu = MarketInstance.objects.get(id = id).determine_result_algo
                if resu =='R':
                    resu = random.randint(1,2)
                    print('R RESU',resu)

                print('RESSU',resu)
                sleep((30))
                Result.objects.create(market_id = id ,resu =resu ,cumgain_id = 1)  #  updates accounts for win lose
                sleep(1) # 5 SEC
                id =id +1

    except Exception as e:
        print('CONTROL ERROR',e)
        return e

control()