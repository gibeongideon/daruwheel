
from time import sleep
from celery import shared_task


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
    from gwheel.models import WheelSpin
    # from core.models import BetSettingVar
    
    id = max([obj.id for obj in WheelSpin.objects.all()])
    try:
     
        from gwheel.models import WheelSpin ,Result
        from core.models import BetSettingVar
   
        print('Processing Results and ')
        try:
            Result.objects.create(market_id = id,cumgain_id =1 )  #  process result of last ma
        except:
            pass

        print('Creating Wheel Spin Instance')
        sleep(2)
        WheelSpin.objects.create(id = id+1) # create WheeSpin of id current +1
        print(f'Market Instance of ID {id+1} created')
        print('ACTIVE BETTING')

        # countD((sleep_time*60))

        id =id +1

    except Exception as e:
        print('CONTROL ERROR',e)
        return e


@shared_task 
def create_spinwheel():
    ''' wheel instance to be executed every 10 minutes'''

    print('Wanna SPIN CREATED')
    control()
    # countD((4.5*60))
    print('SPIN SPIN!! ')
     