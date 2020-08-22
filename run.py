
from users.models import MarketInstance ,Result,BetSettingVar
from time import sleep
import random

def control():
    id = max([MarketInstance.objects.get(id =obj.id).id for obj in MarketInstance.objects.all()]) + 1
    try:
        while True:
                sleep_time = BetSettingVar.objects.get(id =1).results_at
                MarketInstance.objects.create(id = id)
                print('Market Instance Created')
                print(f'SLEEP TIME:{sleep_time}')
                sleep((sleep_time*60))
                print('getting  BACKGROUNG results')
                sleep((10))
                Result.objects.create(market_id = id )  #  updates accounts for win lose
                sleep(1)  # 5 SEC
                id =id +1

    except Exception as e:
        print('CONTROL ERROR',e)
        return e

control()