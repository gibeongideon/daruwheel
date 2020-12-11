# from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from gwheel.models import Result
from channels.layers import get_channel_layer
# from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Result)
def on_results_save(sender, **kwargs):
    print('RESULT SAVES,INSIDE SIGNAL')
    resu = Result.objects.get(id=96).resu  # fix id
    message = f'I got you man from signal bro.You nailed it!RESU{resu}'

    channel_layer = get_channel_layer()
    print(f'MESIN{message}')

    async_to_sync(channel_layer.group_send)(
        "chat_lobby",
        {
            "type": "chat_message",
            "message": message
        }
    )
  