
from time import sleep
from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def countD(n, str1="Market Active till {} count down is ZERO."):
    countDown = n
    while (countDown >= 0):
        cc = []
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
    
    
    try:
        id = max([obj.id for obj in WheelSpin.objects.all()])
        from gwheel.models import WheelSpin ,OutCome
        from core.models import BetSettingVar
   
        print('Processing Results for gamblers accounts!! ')
        try:
            OutCome.objects.create(market_id = id )  #  process result of last ma
        except Exception as e:
            print('OutCOMEerror',e)
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




# def countC(n, str1="Spin in {}"):
#     countDown = n
    
#     while (countDown >= 0):
#         print('Channeling value')

#         cc = []
#         if countDown != 0:
#             channeled_timer(countDown)

#             cc.append(countDown)
#             print(str1.format(cc[0]),end='\r')
#             sleep(1)
#             cc.clear()
#             countDown = countDown - 1
#         else:
#             break 


# channel_layer = get_channel_layer()
# def channeled_timer(secondvalu):

#     # channel_layer = get_channel_layer()
#     print(f'MESIN{secondvalu}')

#     async_to_sync(channel_layer.group_send)(
#         "daru_spin",
#         {
#             "type": "chat_message",
#             "secondvalu": secondvalu,
#         }
#     )

# @shared_task
# def start_count_down():
#     ''' precise spin timer task'''
#     countC(300)
   



