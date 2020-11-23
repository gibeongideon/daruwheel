
# from users.models import MarketInstance ,Result,BetSettingVar
from time import sleep
import random

def countD(n,str1="Market Active till {} count down is ZERO."):
    countDown = n
    while (countDown >= 0):
        cc=[]
        if countDown != 0:
            cc.append(countDown)
            print(str1.format(cc[0]),end='\r')
            sleep(1)
            cc.clear()
            countDown = countDown - 1
        else:
            break  




def control():
    # from users.models import MarketInstance ,Result,BetSettingVar
    # id = max([MarketInstance.objects.get(id =obj.id).id for obj in MarketInstance.objects.all()]) + 1
    try:
        while True:
                from users.models import MarketInstance ,Result,BetSettingVar # import changes in real time
                id = max([MarketInstance.objects.get(id =obj.id).id for obj in MarketInstance.objects.all()]) + 1
                try:
                    Result.objects.create(market_id = id-1,cumgain_id =1 )
                except:
                    pass

                countD(60,str1='Next Market to be created in {} seconds')
                sleep_time = BetSettingVar.objects.get(id =1).results_at
                MarketInstance.objects.create(id = id)
                print(f'Market Instance of ID {id} created')
                print('ACTIVE BETTING')
                print(f'SLEEP TIME:{sleep_time}')

                countD((sleep_time*60))

                print('getting  BACKGROUNG results')
                sleep((5))
                Result.objects.create(market_id = id,cumgain_id =1 )  #  updates accounts for win lose

                id =id +1

    except Exception as e:
        print('CONTROL ERROR',e)
        return e

control()