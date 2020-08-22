#  Copyright August 2020 gideongibeon. All rights reserved.
#  Use of this source code is governed by a BSD-style license that can be
#  found in the LICENSE file.

from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum ,Count, Sum, F ,OuterRef
from datetime import datetime, timedelta ,timezone


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class UserDetail(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='users',blank =True,null=True)
    mobile_no = models.CharField(max_length=10, blank=True,null=True)

    def __str__(self):
        return self.user.username

class Account(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_accounts',blank =True,null=True)
    number = models.CharField(max_length =200,blank=True,null=True)
    balance =models.FloatField(default = 0)
    active = models.BooleanField(default= True)

    def __str__(self): 
        return f'Account No: {self.number} Balance: {self.balance}'

    def save(self, *args, **kwargs):

        try:
            UserDetail.objects.update_or_create(user_id = self.user_id)
            if not self.number:
                import random
                r_no = random.randint(1000,9999)
                self.number = '666' + str(r_no) + str(self.user)

        except Exception as e :
            return e

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('user_id',)
        # unique_together = (['user', 'number',])

class Balance (TimeStamp):
    user_bal = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_balances',blank =True,null=True) # NOT CASCADE #CK
    amount = models.FloatField(max_length=100,default = 0)
    now_bal = models.FloatField(max_length=100,default = 0)
    trans_type = models.CharField(max_length=200 ,blank =True,null=True)
    
    def __str__(self):
        return f'User {self.user_bal}:{self.amount}'

    @property
    def account_bal(self):
        try:
            ac_bal = Account.objects.get(user_id =self.user_bal_id).balance
            return ac_bal
        except Exception as e:
            return e   

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        if not self.pk:
            try:
                self.now_bal = self.account_bal 

            except Exception as e:
                return e

        super().save(*args, **kwargs)


class CashDeposit(TimeStamp):
    user_depo = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_deposits',blank =True,null=True)
    amount = models.FloatField(max_length=10,default=0 ) 
    source_no = models.IntegerField(blank =True ,null= True)
    deposited = models.BooleanField(blank =True ,null= True)
    user_record_done = models.BooleanField(blank =True ,null= True)
    
    def __str__(self):
        return str(self.amount)
    
    @property
    def current_bal(self): 
        try:
            ac_bal = Account.objects.get(user_id =self.user_depo_id).balance
            return ac_bal
        except Exception as e:
            return e

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        # if self.pk:
        try:
            if not self.user_depo_id: # create  user on deposit  and account
                created_user_name = str(self.source_no)
                User.objects.create(username = created_user_name ,password ='27837185gg')
                self.user_depo_id = User.objects.get(username = created_user_name).id

            if not self.deposited:
                try:
                    Account.objects.get(user_id = self.user_depo_id) # if  Account matching query does not exist
                except:
                    Account.objects.create(user_id = self.user_depo_id)  # create account

                ctotal_balanc = Account.objects.get(user_id = self.user_depo_id).balance
                new_bal = ctotal_balanc + self.amount

                Account.objects.filter(user_id=self.user_depo_id).update(balance= new_bal)
                self.deposited = True

            try:
                if not self.user_record_done:
                    Balance.objects.create(user_bal_id =self.user_depo_id,amount= self.amount ,trans_type = 'Deposit')
                    self.user_record_done = True
            except  Exception as e:
                pass
            
        except Exception as e:
            print('DEPOSIT ERROR',e)
            return e

        super().save(*args, **kwargs)


class CashWithrawal(TimeStamp): # sensitive transaction
    user_withr = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='user_withrawals',blank =True,null=True)
    amount = models.FloatField(max_length=10,default=0 ) 
    withrawned = models.BooleanField(blank= True,null =True)
    user_record_done = models.BooleanField(blank= True,null =True)
    # charges_fee = models.FloatField(default =0 ,blank = True,null= true)

    def __str__(self):
        return str(self.amount)

    @property
    def current_bal(self):
        try:
            ac_bal = Account.objects.get(user_id =self.user_withr_id).balance
            return ac_bal
        except Exception as e:
            return e  

    @property # TODO no hrd coding
    def charges_fee(self):
        if self.amount <=100:
            return 10
        elif self.amount <=200:
            return 15
        else:
            return 30

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        account_is_active = Account.objects.get(user_id = self.user_withr_id).active
        # withraw if 
        if account_is_active:# withraw cash ! or else no cash!
            # if self.pk:
            try:
                if not self.withrawned:# withraw cash ! no repeated withraws!
                    ctotal_balanc = Account.objects.get(user_id = self.user_withr_id).balance
                    charges_fee = self.charges_fee

                    if ctotal_balanc > ( self.amount + charges_fee):
                        new_bal = ctotal_balanc - self.amount - charges_fee
                        # self.current_bal = new_bal
                        Account.objects.filter(user_id=self.user_withr_id).update(balance= new_bal)
                        self.withrawned = True # transaction done

                    else:
                        return 'insufficient funds in your account'
                        
                    try:
                        if not  self.user_record_done:
                            Balance.objects.create(user_bal_id =self.user_withr_id,amount= self.amount ,trans_type = 'Withrawal')
                            self.user_record_done = True
                    except:
                        pass

            except Exception as e:
                return  # incase of error /No withrawing should happen
                # pass

            super().save(*args, **kwargs)


class MarketSelection (models.Model):
    ''' Allow creation of additional market /expand application'''
    name = models.CharField(max_length=200, blank =True,null=True)
    odds = models.FloatField(max_length=10 ,blank =True,null=True )

    def __str__(self):
        return f'Selection :{self.name} '


class Stake (models.Model):
    user_stake = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_stakes',blank =True,null=True)
    # balanc = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='sbalances')
    marketinstant = models.ForeignKey('MarketInstance', on_delete=models.CASCADE,related_name='marketinchoices')
    marketselection = models.ForeignKey(MarketSelection, on_delete=models.CASCADE,related_name='marketselections',blank =True,null=True)
    current_bal = models.FloatField(max_length=10,default=0 )
    amount = models.FloatField(max_length=10,default=0 ) 

    outcome = models.CharField(max_length=200,blank =True,null=True)

    start_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    ends_at = models.DateTimeField(auto_now=True,blank =True,null=True)


    stake_placed = models.BooleanField(blank =True,null=True)
    user_record_done = models.BooleanField(blank =True,null=True)


    def __str__(self):
        return f'Stake:{self.amount} for:{self.user_stake}'   

    @property
    def account_bal(self):
        try:
            ac_bal = Account.objects.get(user_id =self.user_stake_id).balance
            return ac_bal
        except Exception as e:
            return e   

    @property
    def place_bet_is_active(self):
        return self.marketinstant.place_stake_is_active

    
    def update_account_on_win_lose(self):

        selection = self.marketselection_id
        try:
            results = Result.objects.get(market_id = self.marketinstant_id).resu  #self.marketinstant.determine_result_algo
        except:
            results = None
        resu = ''
        try:
            if results == None :
                resu = 'PENDING'               
            elif selection == results:
                resu= 'YOU WIN'
            else:
                resu = 'YOU LOSE'
            return resu
            
        except Exception as e:
            print('GERR',e)

    
    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        if self.place_bet_is_active:
            try:
                ctotal_balanc = Account.objects.get(user_id = self.user_stake_id).balance
                if self.amount <= ctotal_balanc:
                    if not self.stake_placed:
                        new_bal = ctotal_balanc - self.amount
                        self.current_bal = new_bal
                        Account.objects.filter(user_id=self.user_stake_id).update(balance= new_bal)
                        self.stake_placed = True

                else:
                    return 'Not enough balance to stake'

                try:
                    if not  self.user_record_done:
                        Balance.objects.create(user_bal_id =self.user_stake_id,amount= self.amount ,trans_type = 'Stake')
                        self.user_record_done = True
                except:
                    pass

            except Exception as e:
                return

            super().save(*args, **kwargs)


class MarketInstance(models.Model):
    amount_stake_per_market = models.FloatField(max_length=100,blank =True,null=True)  # not needed

    created_at = models.DateTimeField(default =datetime.now,blank =True,null=True)
    bet_expiry_time = models.DateTimeField(blank =True,null=True)

    closed_at =  models.DateTimeField(blank =True,null=True)
    results_at =  models.DateTimeField(blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    result = models.IntegerField(blank =True,null= True)

    closed = models.BooleanField(blank =True,null= True)
    

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
            if total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return  0
            
        except Exception as e:
            return e

    @property
    def white_bet_amount(self):

        try:
            total_amount = Stake.objects.filter(marketinstant_id = self.id ).filter(marketselection_id = 2).aggregate(bet_amount =Sum('amount'))
            if  total_amount.get('bet_amount'):
                return total_amount.get('bet_amount')
            return 0
            
        except Exception as e:
            return e

    @property
    def offset(self):
        try:
            return abs(self.white_bet_amount - self.black_bet_amount)

        except Exception as e:
            return 0

    @property
    def gain_after_relief(self):
        per_to_return = BetSettingVar.objects.get(id = 1).per_return
        return ((100 - per_to_return)/100)*self.offset

    @property
    def determine_result_algo(self):  # fix this
        try:
            B = self.black_bet_amount
            W = self.white_bet_amount
            
            if self.instance_is_active == False:
                if B == W:
                    return 'R' # fix me to get random 1 or 2
                if B > W :
                    return 2
                return 1

        except Exception as e:
            return  e

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        # if self.pk:
        try:
            set_up = BetSettingVar.objects.get(id =1)# Set up variables

            self.bet_expiry_time = self.created_at + timedelta(minutes =set_up.bet_expiry_time)
            self.closed_at = self.created_at + timedelta(minutes = set_up.closed_at)
            self.results_at = self.created_at + timedelta(minutes =set_up.results_at)

        except Exception as e:
            return e

        super().save(*args, **kwargs) 


class CumulativeGain(models.Model):

    gain = models.FloatField(default=0, blank =True,null= True)

    @property
    def gainovertime(self):
        pass


class Result(TimeStamp):

    market = models.OneToOneField(MarketInstance,on_delete=models.CASCADE,related_name='rmarkets',blank =True,null= True)
    cumgain = models.ForeignKey(CumulativeGain,on_delete=models.CASCADE,related_name='gains',blank =True,null= True)

    resu = models.FloatField(blank =True,null= True)
    closed = models.BooleanField(blank =True,null= True)
    

    def per_return(self,all_gain,user_stake,all_lose_stake,per_to_return):
        return_amount = (per_to_return/100)*all_gain
        per_user_return = (user_stake/all_lose_stake)*return_amount
        return per_user_return

    def update_acc_n_bal_record(self,user_id,new_bal,amount,trans_type):
        Account.objects.filter(user_id =user_id).update(balance= new_bal)
        Balance.objects.create(user_bal_id =user_id,amount= amount ,trans_type = trans_type) 
    
    def save(self, *args, **kwargs):  
        ''' Overrride internal model save method to update balance on staking  '''
        self.resu = self.market.determine_result_algo

        if  self.resu and  not self.closed:
            try:
                for _stake in Stake.objects.filter(marketinstant = self.market).all(): 
                    user_id = _stake.user_stake_id

                    for  user_stake in Stake.objects.filter(id = _stake.id ): # 
                        ctotal_balanc = Account.objects.get(user_id = user_id).balance
                        amount = user_stake.amount

                        if user_stake.marketselection_id == self.resu:
                            new_bal = ctotal_balanc + amount*2 
                            amount = amount*2
                            trans_type = 'WIN' 
                            self.update_acc_n_bal_record(user_id,new_bal,amount,trans_type)

                        elif user_stake.marketselection_id != self.resu:
                            all_gain = self.market.offset
                            userstake =  user_stake.amount
                            if self.resu == 2:
                                all_lose_stake = self.market.black_bet_amount
                            elif self.resu ==1:
                                all_lose_stake =self.market.white_bet_amount

                            per_to_return = BetSettingVar.objects.get(id = 1).per_return # 

                            relief_amount = self.per_return(all_gain,userstake,all_lose_stake,per_to_return)
                            new_bal = ctotal_balanc + relief_amount
                            amount= relief_amount
                            trans_type = 'Relief On LOSE'
                            self.update_acc_n_bal_record(user_id,new_bal,amount,trans_type)  
                                                                                          
                    self.closed= True

                super().save(*args, **kwargs) #save only if 

            except Exception as e:
                print('RRRRRR',e)
                return

        # super().save(*args, **kwargs)

class WhoWinsAlgo(object):

    def vfl_basic(self):
        pass
 
class BetSettingVar(TimeStamp):
    per_return = models.FloatField(default = 0,blank =True,null= True)
    bet_expiry_time = models.FloatField(default =7,blank =True,null= True)
    closed_at = models.FloatField(default =8,blank =True,null= True)
    results_at = models.FloatField(default =8.1,blank =True,null= True)