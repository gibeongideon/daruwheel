from django.db import models

# from django.conf import settings
# from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import transaction


# User Profile
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
        

    def autogen_account_no(self):
        import random
        return random.randint(10000,99999)

    def save(self, *args, **kwargs):
        try:
            self.number = str(self.user)+str(self.autogen_account_no())
        except Exception as e :
            print('EE',e)
            return
            # return 'failed to create account'
            # pass
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('id',)
        # unique_together = (['user', 'number',])

class Balance (TimeStamp):
    acount = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='accounts')
    total_balance = models.FloatField(max_length=100,default = 0)
    
    def __str__(self):
        return f'Balance of :{str(self.acount)} is {self.total_balance}'
        

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on staking  '''
        # if self.pk:
        try:
            ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
            if self.amount < ctotal_balanc:
                new_bal = ctotal_balanc - self.amount
                self.current_bal = new_bal
                Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
            
            else:
                return 'Not enough balance to stake'

        except Exception as e:
            print('EEE:',e)
            # pass

        super().save(*args, **kwargs) 


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
            CHARGESFEE = 10
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


# MARKET PLACE HERE

class MarketType (models.Model):
    name = models.CharField(max_length=200 )
    def __str__(self):
        return f'Market :{self.name}'


class MarketSelection (models.Model):
    ''' Allow creation of additional market /expand application'''
    markt = models.ForeignKey(MarketType, on_delete=models.CASCADE,related_name='marketsel')
    name = models.CharField(max_length=200 )
    odds = models.FloatField(max_length=10 )
    def __str__(self):
        return f'Selection :{self.name} of {self.markt}'


class MarketChoice(models.Model):# Time track set time limits when market is active/ allow bets when active/block bets when market is in active//
    ''' Allow creation of additional market /expand application'''
    name = models.CharField(max_length=200 )
    markt = models.ForeignKey(MarketSelection, on_delete=models.CASCADE,related_name='cmarket')
    name = models.CharField(max_length=200 ,blank= True,null=True)

    def __str__(self):
        return f'Choice :{str(self.markt)}'


 # END MARKET

class Stake (TimeTrack):
    balanc = models.ForeignKey(Balance, on_delete=models.CASCADE,related_name='sbalances')
    marketchoice = models.ForeignKey(MarketChoice, on_delete=models.CASCADE,related_name='marketchoices')
    current_bal = models.FloatField(max_length=10,default=0 )
    amount = models.FloatField(max_length=10,default=0 ) 
    outcome = models.BooleanField(blank =True,null=True)
    
    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):

        ''' Overrride internal model save method to update balance on staking  '''
        # if self.pk:
        try:
            ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
            if self.amount <= ctotal_balanc:
                new_bal = ctotal_balanc - self.amount
                self.current_bal = new_bal
                Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
            
            else:
                return 'Not enough balance to stake'

        except Exception as e:
            return e
            # pass

        super().save(*args, **kwargs)


class Bet(TimeTrack): # Facade for  bet session
    name = models.OneToOneField(MarketType, on_delete=models.CASCADE,related_name='marketss')

    balanc = models.ForeignKey(Stake, on_delete=models.CASCADE,related_name='shbalances')
    marketchoice = models.ForeignKey(MarketChoice, on_delete=models.CASCADE,related_name='marksetchoices')
    current_bal = models.FloatField(max_length=10,default=0 )
    amount = models.FloatField(max_length=10,default=0 ) 
    
    def __str__(self):
        return str(self.amount)

    # def save(self, *args, **kwargs):

#         ''' Overrride internal model save method to update balance on staking  '''
#         # if self.pk:
#         try:
#             ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
#             if self.amount <= ctotal_balanc:
#                 new_bal = ctotal_balanc - self.amount
#                 self.current_bal = new_bal
#                 Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
            
#             else:
#                 return 'Not enough balance to stake'

#         except Exception as e:
#             return e
#             # pass

#         super().save(*args, **kwargs)


# class Market(TimeTrack): # Facade for  bet session
#     name = models.OneToOneField(MarketType, on_delete=models.CASCADE,related_name='marketss')

#     balanc = models.ForeignKey(Stake, on_delete=models.CASCADE,related_name='shbalances')
#     marketchoice = models.ForeignKey(MarketChoice, on_delete=models.CASCADE,related_name='marksetchoices')
#     current_bal = models.FloatField(max_length=10,default=0 )
#     amount = models.FloatField(max_length=10,default=0 ) 
    
#     def __str__(self):
#         return str(self.amount)

#     def save(self, *args, **kwargs):

#         ''' Overrride internal model save method to update balance on staking  '''
#         # if self.pk:
#         try:
#             ctotal_balanc = Balance.objects.get(id = self.balanc_id).total_balance
#             if self.amount <= ctotal_balanc:
#                 new_bal = ctotal_balanc - self.amount
#                 self.current_bal = new_bal
#                 Balance.objects.filter(id=self.balanc_id).update(total_balance= new_bal)
            
#             else:
#                 return 'Not enough balance to stake'

#         except Exception as e:
#             return e
#             # pass

#         super().save(*args, **kwargs)



class BetInstance(object):
     
    
