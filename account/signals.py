from django.dispatch import receiver
from django.db.models.signals import post_save
# from  users.models import User
from .models import Account
from mpesa_api.models import OnlineCheckoutResponse
from .models import update_account_bal_of ,current_account_bal_of,log_record
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender= User) 
def create_user_account(sender,instance,created, **kwargs):
    if created:
        Account.objects.update_or_create(user=instance)
        print(f'User{instance.username} Account Created ')


@receiver(post_save, sender= OnlineCheckoutResponse) #TODO
def update_account_balance_on_mpesa_deposit(sender,instance,created, **kwargs):
    # if created:
    try:
        if int(instance.result_code) ==200:  ##TODO phone NO detection should be flexible enough
            deposited_amount = instance.amount #NN

            phone_no = str(instance.phone)

            print(f'phone{phone_no}') # debug
            
            this_user = User.objects.get(phone_number = phone_no) 

            new_bal = current_account_bal_of(this_user) + float(deposited_amount) # F2 # fix unsupported operand type(s) for +: 'float' and 'decimal.Decimal'
            update_account_bal_of(this_user,new_bal) #F3
            log_record(this_user.id,deposited_amount,"mpesa online deposit")
            
    except Exception as e:
        print('MPESA DEPO',e)
