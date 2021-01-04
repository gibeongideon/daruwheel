from django.db import models
# from django.contrib.auth.models import User
from core.models import TimeStamp,BetSettingVar
from django.conf import settings
# from .functions import log_record ##NO circular import
class Account(TimeStamp):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_accounts',blank =True,null=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_deposits',blank =True,null=True)
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    deposited = models.BooleanField(blank =True ,null= True)
    has_record = models.BooleanField(blank =True ,null= True)

    class Meta:
        db_table = "d_deposits"
    
    def __str__(self):
        return str(self.amount)
    
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_withrawals',blank =True,null=True)
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0) 
    approved = models.BooleanField(default=False,blank= True,null =True)
    withrawned = models.BooleanField(blank= True,null =True)
    has_record = models.BooleanField(blank= True,null =True)
    active = models.BooleanField(default =True,blank= True,null =True)

    class Meta:
        db_table = "d_withrawals"

    def __str__(self):
        return str(self.amount)

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
