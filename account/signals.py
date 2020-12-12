# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from mpesa_api.models import C2BRequest


# @receiver(post_save, sender=C2BRequest)
# def on_mpesa_c2b_request_save(sender, **kwargs):
#     print('on_mpesa_c2b_request_save')
    


#     latest_resu_id = max([obj.id for obj in Result.objects.all()])
#     resu = Result.objects.get(id=latest_resu_id).resu  # fix id
#     message = resu