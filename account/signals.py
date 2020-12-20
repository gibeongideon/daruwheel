# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from mpesa_api.models import C2BRequest


# @receiver(post_save, sender=C2BRequest)
# def on_mpesa_c2b_request_save(sender, **kwargs):
#     print('on_mpesa_c2b_request_save')
    


#     latest_resu_id = max([obj.id for obj in Result.objects.all()])
#     resu = Result.objects.get(id=latest_resu_id).resu  # fix id
#     message = resu


from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Account



@receiver(post_save, sender= User) 
def create_user_account(sender,instance,created, **kwargs):
    if created:
        Account.objects.update_or_create(user=instance)
        print(f'User{instance.username} Account Created ')
