from django.dispatch import receiver
from django.db.models.signals import post_save
from gwheel.models import Result,OutCome
from channels.layers import get_channel_layer
# from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from time import sleep



@receiver(post_save, sender=OutCome)
def on_results_save(sender,instance, **kwargs):
    print('RESULT SAVES,INSIDE SIGNAL')

    resu = instance.pointer  # fix id
    print(f'RESUUSS{resu}')
    
    try:
        channel_layer = get_channel_layer()
        print(f'MESIN{resu}')

        async_to_sync(channel_layer.group_send)(
            "daru_spin",
            {
                "type": "chat_message",
                "message": resu
            }
        )
    except Exception as ce:
        print(f'Channel error:{ce}')
        pass

    try:
        Result.objects.update_or_create(market_id = instance.market_id,cumgain_id =1 )

    except Exception as re:
        print(f'REESignal error:{re}')
        pass