# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import User
from account.models import Account,TransactionLog

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null= True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null= True)
    is_active = models.BooleanField(default=True, blank=True,null= True)
    is_deleted = models.BooleanField(default=False, blank=True,null= True)

    class Meta:
        abstract = True


class PaymentTransaction(models.Model):
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)

    checkoutRequestID = models.CharField(max_length=100,blank=True,null= True)

    isFinished = models.BooleanField(default=False,blank=True,null= True)
    isSuccessFull = models.BooleanField(default=False,blank=True,null= True)

    trans_id = models.CharField(max_length=30,blank=True,null= True)
    order_id = models.CharField(max_length=200,blank=True,null= True)

    date_modified = models.DateTimeField(auto_now=True,blank=True,null= True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    account_updated = models.BooleanField(default=False,blank=True,null= True)
    has_record = models.BooleanField(default=False,blank=True,null= True)
    closed = models.BooleanField(default=False,blank=True,null= True)

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)

    @property
    def user_id(self):
        user_name = str(self.phone_number).strip()
        return User.objects.get(username= user_name)
    

    # def updateWallet(self):
    #     try:
    #         Wallet.objects.get(phone_number = self.phone_number) 
    #     except:
    #         Wallet.objects.create(phone_number = self.phone_number) 

    #     ctotal_balanc = Wallet.objects.get(phone_number = self.phone_number).available_balance
    #     new_bal = ctotal_balanc + self.amount

    #     Wallet.objects.filter(phone_number=self.phone_number).update(available_balance= new_bal)

    def updateAccount(self):
        try:
            print(self.user_id)
            ctotal_balanc = float(Account.objects.get(user = self.user_id).balance)
            new_bal = ctotal_balanc + float(self.amount)

            Account.objects.filter(user=self.user_id).update(balance= new_bal)
         
        except Exception as e:
            print('TRANS Account update issue',e)
            raise Exception('Failed to update account',e)
            

    def log_record(self,destin):
        try:
            TransactionLog.objects.update_or_create(user =self.user_id,amount= self.amount ,trans_type = f'{destin}')
        except  Exception as e:
            print('LOGG',e)
        
            
    def save(self, *args, **kwargs):
             
        ''' Overrride internal model save method to update in account  mpesa deposit staking  '''
        if not self.closed:
            try:
                if self.isSuccessFull and not self.account_updated:
                    try:
                        self.updateAccount()
                        self.account_updated = True
                        self.closed =True
        
                    except Exception as e:
                        print('Mpesa-> Acount Err',e)

                    try:
                        self.log_record('Mpesa deposit')
                        self.has_record = True
                    except Exception as e:
                        print('Mpesa-> Account Err',e)
                
            except Exception as e:
                print('RefCredit:',e)
                return 
            super().save(*args, **kwargs)


# class Wallet(BaseModel):
#     phone_number = models.CharField(max_length=30)
#     available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
#     actual_balance = models.DecimalField(('actual_balance'), max_digits=6, decimal_places=2, default=0)
#     date_modified = models.DateTimeField(auto_now=True, null=True)
#     date_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

#     def __str__(self):
#         return self.phone_number
