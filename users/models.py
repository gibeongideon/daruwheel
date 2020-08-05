#  Copyright August 2020 gideongibeon. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the LICENSE file.



from django.db import models
# from django.conf import settings
# from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum ,Count, Sum, F ,OuterRef
from datetime import datetime, timedelta ,timezone
# import math


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class TimeTrack(models.Model):
    start_at = models.DateTimeField(auto_now_add=False,blank =True,null=True)
    ends_at = models.DateTimeField(auto_now=False,blank =True,null=True)
    is_active = models.BooleanField(default=False,blank =True,null=True)

    class Meta:
        abstract = True

class CustomUser(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='users')
    mobile_no = models.CharField(max_length=10,unique = True, blank=True,null=True)

    def __str__(self):
        return self.user.username


class Account(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='vfluser')
    number = models.CharField(max_length=2000 ,default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default= True)

    def __str__(self):
        return f'Account of User: {str(self.user)}'

    def autogen_account_no(self): # fix
        import random
        return random.randint(10000,99999)

    def save(self, *args, **kwargs):
        try:
            self.number = str(self.user)+str(self.autogen_account_no())
        except Exception as e :
            print('EE',e)
            return

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('id',)
        # unique_together = (['user', 'number',])

class Balance (TimeStamp):
    acount = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='accounts')
    total_balance = models.FloatField(max_length=100,default = 0)
    
    def __str__(self):
        return f'Balance of :{str(self.acount)} is {self.total_balance}'
    

class CashDeposit(TimeStamp):
    balanc = models.ForeignKey(Balance, on_delete=models.CASCADE,related_name='cbalances')
    amount = models.FloatField(max_length=10,default=0 ) 
    
    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        # if self.pk:
        try:
            ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
            new_bal = ctotal_balanc + self.amount
            # self.current_bal = new_bal
            Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
            
        except Exception as e:
            print('EEE:',e)
            return e
            # pass

        super().save(*args, **kwargs)


class CashWithrawal(TimeStamp):
    balanc = models.ForeignKey(Balance, on_delete=models.CASCADE,
                                related_name='wbalances')
    # current_bal = models.FloatField(max_length=10,default=0 )
    amount = models.FloatField(max_length=10,default=0 ) 
    
    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        # if self.pk:
        try:
            ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
            #  dirty code down there ; fix it
            if self.amount < 50:
                CHARGESFEE = 5
            elif self.amount <200:
                CHARGESFEE = 10
            else:
                CHARGESFEE =25
            if ctotal_balanc > ( self.amount + CHARGESFEE):
                new_bal = ctotal_balanc - self.amount - CHARGESFEE
                # self.current_bal = new_bal
                Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
            else:
                return 'insufficient funds in your account'

        except Exception as e:
            print('EEE:',e)
            # pass

        super().save(*args, **kwargs)


class MarketSelection (models.Model):
    ''' Allow creation of additional market /expand application'''
    # markt = models.ForeignKey(MarketType, on_delete=models.CASCADE,related_name='marketsel')
    name = models.CharField(max_length=200, blank =True,null=True)
    odds = models.FloatField(max_length=10 ,blank =True,null=True )

    def __str__(self):
        return f'Selection :{self.name} '


class Stake (models.Model):
    balanc = models.ForeignKey(Balance, on_delete=models.CASCADE,related_name='sbalances')
    marketinstant = models.ForeignKey('MarketInstance', on_delete=models.CASCADE,related_name='marketinchoices')
    marketselection = models.ForeignKey(MarketSelection, on_delete=models.CASCADE,related_name='marketselections',blank =True,null=True)
    current_bal = models.FloatField(max_length=10,default=0 )
    amount = models.FloatField(max_length=10,default=0 ) 

    outcome = models.CharField(max_length=200,blank =True,null=True)

    start_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    ends_at = models.DateTimeField(auto_now=True,blank =True,null=True)

    account_apdated = models.BooleanField(default= False)

    account_apdated_flag = False




    def __str__(self):
        return str(self.amount)
    

    @property
    def place_bet_is_active(self):
        return self.marketinstant.place_stake_is_active

    # @property
    # def get_result_is_active(self):
    #     return self.marketinstant.get_result_active



    # @property
    # def account_apdated(self):
    #     self.account_updated  = None
    #     return self.account_apdated

    

          
        



    def update_account_on_win_lose(self):



        selection = self.marketselection_id
        results = self.marketinstant.determine_result_algo
        resu = ''
      
        try:

            if results == 0 :
                resu = 'Pending'               
            if selection == results:
                resu= 'YOU WIN'
            else:
                resu = 'YOU LOSE'
            # self.account_apdated = True

            print('FLAGGGG',self.account_apdated_flag)
            print('jjjjj',self.account_apdated)

            # print(self.objects.all())#filter(pk=self.sub_task_id).update(site_trenched_distance=trenched_distance)

            


            

            # if not self.account_apdated():
            #     Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)

        except Exception as e:
            print('GERR',e)

       
    
    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        if self.place_bet_is_active:
            try:
                ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
                if self.amount <= ctotal_balanc:
                    new_bal = ctotal_balanc - self.amount
                    self.current_bal = new_bal
                    Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
                else:
                    return 'Not enough balance to stake'
                 
                # self.analze_bets()

            except Exception as e:
                print(e)
                return
                # pass

            super().save(*args, **kwargs)

class AcountUpdate(models.Model):


    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update account  on bet  win lose  '''
        # if self.pk:
        try:
            self.bet_expiry_time = self.created_at + timedelta(minutes =1)
            self.closed_at = self.created_at + timedelta(minutes =2)
            self.results_at = self.created_at + timedelta(minutes =2.5)

        except Exception as e:
            print(' save ErrEEE:',e)

        super().save(*args, **kwargs) 




class MarketInstance(models.Model):
    amount_stake_per_market = models.FloatField(max_length=100,blank =True,null=True)  # not needed

    created_at = models.DateTimeField(default =datetime.now,blank =True,null=True)
    bet_expiry_time = models.DateTimeField(blank =True,null=True)

    closed_at =  models.DateTimeField(blank =True,null=True)
    results_at =  models.DateTimeField(blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    result = models.IntegerField(blank =True,null= True)
    
    markets = models.ForeignKey('CumulativeGain', on_delete=models.CASCADE,related_name='markets',blank =True,null= True)
    

    def __str__(self):
        return f'MarketInstance({self.id})'

    @property
    def get_result_active(self):
        try:
            if datetime.now(timezone.utc) > self.results_at:# and datetime.now(timezone.utc) > self.closed_at:
                return True
            return False
        except Exception as e:
            return e

    @property
    def instance_is_active(self):
        try:

            if datetime.now(timezone.utc) >  self.created_at and datetime.now(timezone.utc) < self.closed_at:
                return True
            return False
        except Exception as e:
            print(e)
            return e

    @property
    def place_stake_is_active(self):
        try:

            if datetime.now(timezone.utc) <  self.bet_expiry_time and self.instance_is_active:
                return True
            return False
        except Exception as e:
            return e

    @property
    def total_bet_amount_per_marktinstance(self):

        try:

            total_amount = Stake.objects.filter(marketinstant_id = self.id ).aggregate(bet_amount =Sum('amount'))
            self.amount_stake_per_market = total_amount.get('bet_amount')
            return  total_amount.get('bet_amount')

        except Exception as e:
            return e

    @property
    def black_bet_amount(self):
        try:
            total_amount = Stake.objects.filter(marketinstant_id = self.id ).filter(marketselection_id = 1).aggregate(bet_amount =Sum('amount'))
            if total_amount is None:
                return 0
            return  total_amount.get('bet_amount')
            
        except Exception as e:
            print('HEY ASS HOLEBlack',e)
            return e

    @property
    def white_bet_amount(self):

        try:
            
            total_amount = Stake.objects.filter(marketinstant_id = self.id ).filter(marketselection_id = 2).aggregate(bet_amount =Sum('amount'))
            if  total_amount is None:
                return 0
            return  total_amount.get('bet_amount')
            
        except Exception as e:
            print('WHITE ERR',e)
            return e

    @property
    def determine_result_algo(self):
        try:
            if self.instance_is_active == False:

                if self.black_bet_amount > self.white_bet_amount:
                    return 2  # 2 represent WHITE
                return 1 # represent BLACK
            else:
                return 0

        except Exception as e:
            if self.id%2:   # fix me to create random when no bet 
                return 2
            return  1



        



    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        # if self.pk:
        try:
            self.bet_expiry_time = self.created_at + timedelta(minutes =2)
            self.closed_at = self.created_at + timedelta(minutes =3)
            self.results_at = self.created_at + timedelta(minutes =3.5)

        except Exception as e:
            print(' save ErrEEE:',e)

        super().save(*args, **kwargs) 


class CumulativeGain(models.Model):
    gain = models.FloatField(blank =True,null= True)

    @property
    def gainovertime(self):

        try:
            total_amount = MarketInstance.objects.filter(markets_id = self.id ).aggregate(bet_amount =Sum('amount_stake_per_market'))
            return  total_amount.get('bet_amount')

        except Exception as e:
            print('HEYCUM',e)
            return e




# def update_balance_on_win_lose(selection,results,balanc_id,amount,flag = False):

#     odds =2
#     if flag ==False:

#         print('RUNNING EX FUNC')

#         try:           
#             ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
#             odds = 2

#             if selection == results:
#                 new_bal = ctotal_balanc + amount * odds
#                 Balance.objects.filter(id= balanc_id).update(total_balance= new_bal)

#             else:
#                 new_bal = ctotal_balanc - amount 
#                 Balance.objects.filter(id=balanc_id).update(total_balance= new_bal)

#         except Exception as g:
#             print('G err',g)

                    





    # def update_account_on_win_lose(self):

    #     selection = self.marketselection_id
    #     results = self.marketinstant.determine_result_algo

    #     try:

    #         if results == 0 :
    #             return 'Pending'            
                
    #         ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
    #         odds = 2

    #         #self.account_apdated_flag = True

    #         if selection == results:

    #             if not self.account_apdated_flag:
    #                 new_bal = ctotal_balanc + self.amount * odds
    #                 Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)

    #                 self.account_apdated_flag = 'Updated'
                    
    #                 print( 'FLAG',self.account_apdated_flag)

    #             return 'YOU WIN'

    #         else:

    #             if not self.account_apdated_flag :
    #                 new_bal = ctotal_balanc - self.amount

    #                 self.account_apdated_flag = 'Updated'
    #                 Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
                    
    #                 print( 'FLAG',self.account_apdated_flag)

                # return 'YOU LOSE'

            # if not self.account_apdated():
            #     Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)

        # except Exception as e:
            # print('GERR',e)