from django.db import models
# from django.contrib.auth.models import User
from core.models import TimeStamp,BetSettingVar
from django.conf import settings
from .exceptions import NegativeTokens, NotEnoughTokens # LockException,
from decimal import Decimal
import math
from core.models import set_up
from django.core.validators import MinValueValidator
# from .functions import log_record ##NO circular import

class Account(TimeStamp):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_accounts',blank =True,null=True)
    token_count = models.IntegerField(default=0)

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actual_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refer_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    trial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=50000)
    active = models.BooleanField(default= True)

    def __str__(self): 
        return 'Account No: {0} Balance: {1}'.format(self.user,self.balance)
    class Meta:
        db_table = "d_accounts"
        ordering = ('-user_id',)

    def add_tokens(self, number):
        """Increase user tokens amount watch over not to use negative value.

        self -- user whose token_count field  gonna be increased
        number -- tokens amount, must be integer

        In case negative number no changes happened.
        """
        int_num = int(number)
        if int_num > 0:
            self.token_count += int_num
            
    def decrease_tokens(self, number):
        """Decrease user tokens amount watch over not to set negative value.

        Keyword arguments:
        self -- user whose token_count field is to be decreased
        number -- tokens amount, must be integer, cannot be greater
                than token_count

        In case number is greater than user token_count NegativeTokens
        exception raised, otherwise simply decrease token_count with number.
        """
        int_num = int(number)
        if self.token_count - int_num >= 0:
            self.token_count -= int_num
        else:
            raise NegativeTokens()

class Curr_Variable(TimeStamp):
    """Store currencies with specified name and rate to token amount."""

    name = models.CharField(max_length=30,blank =True,null=True)
    curr_unit = models.DecimalField(max_digits=12, decimal_places=5,default= 1)

    def __str__(self):
        """Simply present currency name and it's curr_unit."""
        return str(self.curr_unit)

    # @classmethod
    # def update_curr_unit(cls,value):
    #     try:
    #         cls.objects.get(id=1).update(curr_unit= value)
    #     except Exception as e :
    #         print(f'update_curr_unit{e}')
            

class Currency(TimeStamp):
    """Store currencies with specified name and rate to token amount."""
    common_var = models.ForeignKey(Curr_Variable, on_delete=models.CASCADE,related_name='curr_vars',blank =True,null=True)

    name = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=6,decimal_places=5,blank=True,null= True)
    amount_equip_to_one_ksh =models.FloatField(blank=True,null= True)
    # curr_unit = models.DecimalField(help_text= 'set up variable', max_digits=6, decimal_places=2,default=0,blank=True,null= True)

    def __str__(self):
        """Simply present currency name and it's rate."""
        return self.name + " - " + str(self.rate)

    @classmethod
    def get_tokens_amount(cls, currency_name, value):
        """Convert value in specified currency to tokens.

        Keyword arguments:
        cls -- enable connect to Currency model,
        currency_name -- allow to get specified currency,
        value -- float value represents amount of real money,

        Could raise Currency.DoesNotExist exception.
        Token value is rounded down after value multiplication by rate.
        """
        curr = cls.objects.get(name=currency_name)
        tokens = value * float(curr.rate)
        tokens_floor = math.floor(tokens)
        return tokens_floor

    @classmethod
    def get_withdraw_amount(cls, currency_name, tokens):
        """Convert tokens to amount of money in specified currency.

        Keyword arguments:
        cls -- enable connect to Currency model,
        currency_name -- allow to get specified currency,
        tokens -- integer value represents number of tokens,

        Could raise Currency.DoesNotExist exception and NegativeTokens
        exception.
        Returned object is casted to Decimal with two places precision.
        """
        curr = cls.objects.get(name=currency_name)
        if tokens < 0:
            raise NegativeTokens()

        value = Decimal(round(tokens / float(curr.rate), 2))
        return value

    # @classmethod
    # def update_curr_unit(cls,value):
    #     try:
    #         cls.objects.update(curr_unit= value)
    #     except Exception as e :
    #         print(f'update_curr_unit{e}')
            
    @property
    def to_token_rate(self):
        print('Check')
        print(set_up['curr_unit'])
        try:
            return 1/(float(self.amount_equip_to_one_ksh) * float(self.common_var.curr_unit))
        except Exception as e:
            return e
    class Meta:
        db_table = "d_currency"
        


class RefCredit(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='ref_accountcredit_users',blank =True,null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    current_bal =  models.DecimalField(max_digits=12, decimal_places=2,blank =True,null=True)
    credit_from = models.CharField(max_length=200 ,blank =True,null=True)
    closed = models.BooleanField(blank =True ,null= True)
    has_record = models.BooleanField(blank =True ,null= True)
    approved = models.BooleanField(default =False,blank =True ,null= True)
    class Meta:
        db_table = "d_refcredits"
    
    @property
    def refer_balance(self):
        return float(Account.objects.get(user_id = self.user_id).refer_balance)

    @property
    def min_redeam(self):
        return BetSettingVar.objects.get(id=1).min_redeem_refer_credit #auto create

    def update_refer_balance(self):
        try:
            new_bal = self.refer_balance + float(self.amount)
            self.current_bal = new_bal
            Account.objects.filter(user_id= self.user_id).update(refer_balance= new_bal)
            self.closed = True
            
        except Exception as e:
            print('update_refer_balance',e)
            pass
            
    def tranfer_to_main_account(self):
        try:
            main_balance= current_account_bal_of(self.user_id)#F 
            main_new_bal = self.refer_balance + main_balance

            Account.objects.filter(user_id= self.user_id).update(refer_balance= 0)
            update_account_bal_of(self.user_id,main_new_bal) #F
            log_record(self.user_id,self.refer_balance,'RDM') #F
            self.closed = True

        except Exception as e:
            print('tranfer_to_main_account2',e)
            pass
        self.closed = True        
    
    def save(self, *args, **kwargs):

        ''' Overrride internal model save method to update balance on staking  '''
        # if not self.closed:
        try:
            if not self.closed:
                if self.refer_balance < self.min_redeam:
                    print('Usual Refer Cash')
                    self.update_refer_balance()

                elif self.refer_balance > self.min_redeam and self.approved:
                    print('Updating Account of Refer CASH!')
                    self.tranfer_to_main_account()

            if not self.has_record:
                log_record(self.user_id,self.amount,'RC')

        except Exception as e:
            print('RefCredit:',e)
            return 

        super().save(*args, **kwargs)

class TransactionLog(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_transactions_logs',blank =True,null=True) # NOT CASCADE #CK
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    now_bal = models.DecimalField(('now_bal'), max_digits=12, decimal_places=2, default=0)
    trans_type = models.CharField(max_length=100 ,blank =True,null=True)
    class Meta:
        db_table = "d_trans_logs"
        ordering = ('-created_at',)
    
    def __str__(self):
        return 'User {0}:{1}'.format(self.user,self.amount) 

    @property
    def account_bal(self):
        return current_account_bal_of(self.user_id) #F  Account.objects.get(user_id =self.user_id).balance
        

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        if not self.pk:
            try:
                self.now_bal = self.account_bal 
            except Exception as e:
                print('TransactionLog ERROR:',e)
                pass

        super().save(*args, **kwargs)

class CashDeposit(TimeStamp):
    """Represent single money deposit made by user using 'shop'.
    Define fields to store amount of money, using Decimal field with
    two places precision and maximal six digits, time of deposit creation,
    and connect every deposit with user and used currency.
    """
    # amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    deposited = models.BooleanField(blank =True ,null= True)
    has_record = models.BooleanField(blank =True ,null= True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_deposits',blank =True,null=True)

    currency_id = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank =True,null=True
    )

    def __str__(self):
        """Simply present name of user connected with deposit and amount."""
        return self.user.username + " made " + str(self.amount) + " deposit"

    class Meta:
        db_table = "d_deposits"
    
    @property
    def current_bal(self): 
        return current_account_bal_of(self.user_id)
            

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        # if self.pk:
        try:

            if not self.deposited:
                ctotal_balanc = current_account_bal_of(self.user_id) #F
                new_bal = ctotal_balanc + int(self.amount)
                update_account_bal_of(self.user_id,new_bal) #F
                self.deposited = True

            try:
                if not self.has_record:
                    log_record(self.user_id,self.amount,'Shop Deposit')
                    self.has_record = True
            except  Exception as e:
                pass
            
        except Exception as e:
            print('DEPOSIT ERROR',e)#  issue to fix on mpesa deposit error
            return

        super().save(*args, **kwargs)


class CashWithrawal(TimeStamp): # sensitive transaction
    """Represent user's money withdrawal instance.
    Define fields to store amount of money, using Decimal field with
    two places precision and maximal six digits, time when withdraw is
    signaled and connect every withdraw with user and used currency.
    """
    # amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    address = models.CharField(max_length=100)
    
    approved = models.BooleanField(default=False,blank= True,null =True)
    withrawned = models.BooleanField(blank= True,null =True)
    has_record = models.BooleanField(blank= True,null =True)
    active = models.BooleanField(default =True,blank= True,null =True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_withrawals',blank =True,null=True
        )    
    currency_id = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        )


    def __str__(self):
        """Simply present name of user connected with withdraw and amount."""
        return self.user.username + " want to withdraw " + str(self.amount)

    class Meta:
        db_table = "d_withrawals"

    @property
    def user_account(self):
        return current_account_bal_of(self.user)# Account.objects.get(user_id =self.user_id)
 

    @property # TODO no hrd coding
    def charges_fee(self):
        if self.amount <=100:
            return 0
        elif self.amount <=200:
            return 0
        else:
            return 0

    def withraw_status(self):
        if not self.approved:
            return 'pending'
        elif self.approved and self.withrawned:
            return 'success'
        else:
            return 'failed'

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        account_is_active = self.user_account.active
        ctotal_balanc = self.user_account.balance

        if self.active: # edit prevent # avoid data ma
            if account_is_active:# withraw cash ! or else no cash!
                try:
                    if not self.withrawned and self.approved:# stop repeated withraws and withraw only id approved by ADMIN 
                        charges_fee = self.charges_fee # TODO settings

                        if ctotal_balanc >= ( self.amount + charges_fee):
                            try:                                
                                new_bal = ctotal_balanc - self.amount - charges_fee
                                update_account_bal_of(self.user_id,new_bal) # F
                                self.withrawned = True # transaction done

                                try:
                                    if not self.has_record:
                                        log_record(self.user_id,self.amount,'Withrawal')
                                        self.has_record = True
                                        self.active = False
                                except Exception as e:
                                    print('TRANSWITH:',e)
                                    pass

                            except Exception as e:
                                print('ACCC',e)
         
                except Exception as e:  
                    print('CashWithRawal:',e)
                    return  # incase of error /No withrawing should happen
                    # pass
                if self.approved: #and self.withrawned and self.has_record:
                    self.active =False

                super().save(*args, **kwargs)

# Helper functions

def log_record(user_id,amount,trans_type):# F1
    TransactionLog.objects.update_or_create(user_id =user_id,amount= amount ,trans_type = trans_type)

def current_account_bal_of(user_id): #F2
    try:
        return float(Account.objects.get(user_id =user_id).balance)
    except Exception as e:
        return e

def update_account_bal_of(user_id,new_bal): #F3
    try:
        if new_bal >= 0:
            Account.objects.filter(user_id =user_id).update(balance= new_bal)
        else:
            log_record(user_id,0,'Account Error') # REMOVE
    except Exception as e:
        return e

def refer_credit_create(credit_to_user,credit_from_username,amount):
    try:
        RefCredit.objects.update_or_create(user = credit_to_user,credit_from = credit_from_username, amount= amount)
    except Exception as e:
        print(f'RRR{e}')
