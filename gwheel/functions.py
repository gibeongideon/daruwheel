
from time import sleep
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



def countC(n, str1="Spin in {}"):
    countDown = n

    while (countDown >= 0):
        # print('Channeling value')

        cc = []
        channeled_timer(countDown)
        if countDown != 0:
            cc.append(countDown)
            print(str1.format(cc[0]),end='\r')
            sleep(1)
            cc.clear()
            countDown = countDown - 1
        else:
            break 


def spin_manager():
    from gwheel.models import WheelSpin
    from gwheel.models import WheelSpin ,OutCome
    from core.models import BetSettingVar
    # from core.models import BetSettingVar
    try:
        id = max([obj.id for obj in WheelSpin.objects.all()])
        print('Processing Results for gamblers accounts!! ')
        try:
            OutCome.objects.create(market_id = id)  #  process result of last ma
        except Exception as e:
            print('OutCOMEerror',e)
            pass
        print('Creating Wheel Spin Instance')
        sleep(2)
        WheelSpin.objects.create(id = id+1) # create WheeSpin of id current +1
        print(f'Market Instance of ID {id+1} created')
        # countD((sleep_time*60))
        id =id +1
    except Exception as e:
        print('CONTROL ERROR',e)
        return e



################ web Socket functions ##########

channel_layer = get_channel_layer()
def channeled_timer(secondvalu):
    # channel_layer = get_channel_layer()
    # print(f'VALL:SS{secondvalu}')
    async_to_sync(channel_layer.group_send)(
        "daru_spin",
        {
            "type": "second_value",
            "secondvalu": secondvalu,
        }
    )
