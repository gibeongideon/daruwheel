# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import uuid
from users.models import Account,UserDetail ,Balance
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True


class PaymentTransaction(models.Model):
    phone_number = models.CharField(max_length=30)
    amount = models.DecimalField(('amount'), max_digits=6, decimal_places=2, default=0)
    isFinished = models.BooleanField(default=False)
    isSuccessFull = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30)
    order_id = models.CharField(max_length=200)
    checkoutRequestID = models.CharField(max_length=100)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.phone_number, self.amount)

    @property
    def user_id(self):
        try:
            user_id = UserDetail.objects.get(phone_number = self.phone_number).id
        except:
            self.create_user()
            user_id = User.objects.get(username =self.phone_number).id

            UserDetail.objects.create(user_id = user_id ,phone_number = self.phone_number )

        return user_id

    def create_user(self): # TODO # create actual user that can log in#still a challenge
        print('HEY HEY HEY')
        created_user_name = str(self.phone_number)
        User.objects.create(username = created_user_name ,password ='27837185gg')
        # self.user_depo_id = User.objects.get(username = created_user_name).id


    def updateWallet(self):
        try:
            Wallet.objects.get(phone_number = self.phone_number) 
        except:
            Wallet.objects.create(phone_number = self.phone_number) 

        ctotal_balanc = Wallet.objects.get(phone_number = self.phone_number).available_balance
        new_bal = ctotal_balanc + self.amount

        Wallet.objects.filter(phone_number=self.phone_number).update(available_balance= new_bal)

    def updateAccount(self):

        try:
            try:
                Account.objects.get(user_id = self.user_id)
            except Exception as e:
                print('ACCCRtrans',e)
                Account.objects.update_or_create (user_id = self.user_id)  # create account

            ctotal_balanc = Account.objects.get(user_id = self.user_id).balance
            new_bal = ctotal_balanc + self.amount

            Account.objects.filter(user_id=self.user_id).update(balance= new_bal)
         
        except Exception as e:
            print('TRANS Account update issue',e)
            pass

    def create_bal_record(self,destin):
        try:
            Balance.objects.create(user_bal_id =self.user_id,amount= self.amount ,trans_type = f'Deposit to {destin}')
        except  Exception as e:
            print(e)
            pass


    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        # 
        
        try:
            if not self.closed:
                try:
                    self.updateAccount()
                    self.create_bal_record('Account')
                except Exception as e:
                    print ('account update fails',e)  #what is this for //raise stuff man
                    pass #continue
                # try:
                #     self.updateWallet()
                #     self.create_bal_record('Wallet')

                # except Exception as e:
                #     print ('wallet update fails',e)  #what is this for 
                #     pass #continue

                self.closed = True if self.isFinished and self.isSuccessFull else False # need else realy?

            super().save(*args, **kwargs)
            
        except Exception as e:
            print('TRANSACTION ERROR',e)
            return e

        



class Wallet(BaseModel):
    phone_number = models.CharField(max_length=30)
    available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
    actual_balance = models.DecimalField(('actual_balance'), max_digits=6, decimal_places=2, default=0)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return self.phone_number