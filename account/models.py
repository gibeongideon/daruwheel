from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime, timedelta #,timezone
# from django.utils import timezone

from core.models import TimeStamp,BetSettingVar

class Account(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_accounts',blank =True,null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refer_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    trial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=50000)
    active = models.BooleanField(default= True)

    def __str__(self): 
        return f'Account No: {self.user} Balance: {self.balance}'
    class Meta:
        ordering = ('-user_id',)

class RefCredit(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ref_accountcredit_users',blank =True,null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    current_bal =  models.DecimalField(max_digits=12, decimal_places=2,blank =True,null=True)
    closed = models.BooleanField(blank =True ,null= True)
    has_record = models.BooleanField(blank =True ,null= True)
    approved = models.BooleanField(default =False,blank =True ,null= True)
    
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
            pass
            print('update_refer_balance',e)

    def tranfer_to_main_account(self):
        try:

            main_balance= float(Account.objects.get(user_id = self.user_id).balance)
            main_new_bal = self.refer_balance + main_balance

            Account.objects.filter(user_id= self.user_id).update(refer_balance= 0)
            Account.objects.filter(user_id= self.user_id).update(balance= main_new_bal)

            TransactionLog.objects.create(user_id =self.user_id,amount= self.refer_balance ,trans_type = 'RDM')

            self.closed = True

        except Exception as e:
            print('tranfer_to_main_account2',e)
            pass
        self.closed = True

    def log_record(self):
        try:
            TransactionLog.objects.create(user_id = self.user_id,amount= self.amount ,trans_type = 'RC')
            self.has_record = True
        except Exception as e:
            print('has Record err',e)
            pass
        
    
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
                self.log_record()

        except Exception as e:
            print(f'RefCredit:{e}')
            return 

        super().save(*args, **kwargs)


class TransactionLog(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_balances',blank =True,null=True) # NOT CASCADE #CK
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    now_bal = models.DecimalField(('now_bal'), max_digits=12, decimal_places=2, default=0)
    trans_type = models.CharField(max_length=200 ,blank =True,null=True)
    
    def __str__(self):
        return f'User {self.user}:{self.amount}'

    class Meta:
        ordering = ('-created_at',)

    @property
    def account_bal(self):
        try:
            return Account.objects.get(user_id =self.user_id).balance
        
        except Exception as e:
            return e   

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
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_deposits',blank =True,null=True)
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    source_no = models.IntegerField(blank =True ,null= True)
    deposited = models.BooleanField(blank =True ,null= True)
    has_record = models.BooleanField(blank =True ,null= True)
    
    def __str__(self):
        return str(self.amount)
    
    @property
    def current_bal(self): 
        try:
            return Account.objects.get(user_id =self.user_id).balance
            
        except Exception as e:
            return e

    def save(self, *args, **kwargs):
        ''' Overrride internal model save method to update balance on deposit  '''
        # if self.pk:
        try:
            if not self.user_id: # create  user on deposit  and account
            
                created_user_name = str(self.source_no)
                User.objects.create_user(username = created_user_name ,password ='27837185gg') # FIXED with create_user instead of create
                self.user_id = User.objects.get(username = created_user_name).id

            if not self.deposited:
                try:
                    Account.objects.get(user_id = self.user_id)  # if  Account matching query does not exist
                except:
                    Account.objects.create(user_id = self.user_id)  # create account

                ctotal_balanc = Account.objects.get(user_id = self.user_id).balance
                new_bal = ctotal_balanc + self.amount

                Account.objects.filter(user_id=self.user_id).update(balance= new_bal)
                self.deposited = True

            try:
                if not self.has_record:
                    TransactionLog.objects.create(user_id =self.user_id,amount= self.amount ,trans_type = 'Deposit')
                    self.has_record = True
            except  Exception as e:
                pass
            
        except Exception as e:
            print('DEPOSIT ERROR',e)#  issue to fix on mpesa deposit error
            return

        super().save(*args, **kwargs)


class CashWithrawal(TimeStamp): # sensitive transaction
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_withrawals',blank =True,null=True)
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0) 
    withrawned = models.BooleanField(blank= True,null =True)
    has_record = models.BooleanField(blank= True,null =True)
    # charges_fee = models.FloatField(default =0 ,blank = True,null= true)

    def __str__(self):
        return str(self.amount)

    @property
    def current_bal(self):
        try:
            ac_bal = Account.objects.get(user_id =self.user_id).balance
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
        account_is_active = Account.objects.get(user_id = self.user_id).active
        # withraw if 
        if account_is_active:# withraw cash ! or else no cash!
            # if self.pk:
            try:
                if not self.withrawned:# withraw cash ! no repeated withraws!
                    ctotal_balanc = Account.objects.get(user_id = self.user_id).balance
                    charges_fee = self.charges_fee

                    if ctotal_balanc > ( self.amount + charges_fee):
                        new_bal = ctotal_balanc - self.amount - charges_fee
                        # self.current_bal = new_bal
                        Account.objects.filter(user_id=self.user_id).update(balance= new_bal)
                        self.withrawned = True # transaction done

                    else:
                        return 'insufficient funds in your account'
                        
                    try:
                        if not  self.has_record:
                            TransactionLog.objects.create(user_id =self.user_id,amount= self.amount ,trans_type = 'Withrawal')
                            self.has_record = True
                    except:
                        pass

            except Exception as e:
                print(f'CashWithRawal:{e}')
                return  # incase of error /No withrawing should happen
                # pass

            super().save(*args, **kwargs)