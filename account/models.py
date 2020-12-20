from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStamp,BetSettingVar


class Account(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_accounts',blank =True,null=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ref_accountcredit_users',blank =True,null=True)
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
            print('RefCredit:',e)
            return 

        super().save(*args, **kwargs)


class TransactionLog(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_balances',blank =True,null=True) # NOT CASCADE #CK
    amount = models.DecimalField(('amount'), max_digits=12, decimal_places=2, default=0)
    now_bal = models.DecimalField(('now_bal'), max_digits=12, decimal_places=2, default=0)
    trans_type = models.CharField(max_length=200 ,blank =True,null=True)

    class Meta:
        db_table = "d_trans_logs"
    
    def __str__(self):
        return 'User {0}:{1}'.format(self.user,self.amount)

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

    class Meta:
        db_table = "d_deposits"
    
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
                    TransactionLog.objects.create(user_id =self.user_id,amount= self.amount ,trans_type = 'Shop deposit')
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
    approved = models.BooleanField(default=False,blank= True,null =True)
    withrawned = models.BooleanField(blank= True,null =True)
    has_record = models.BooleanField(blank= True,null =True)
    active = models.BooleanField(default =True,blank= True,null =True)
    # charges_fee = models.FloatField(default =0 ,blank = True,null= true)

    class Meta:
        db_table = "d_withrawals"

    def __str__(self):
        return str(self.amount)

    @property
    def user_account(self):
        try:
            return Account.objects.get(user_id =self.user_id)
        except :
            return 'querying..' 

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
                    
                        charges_fee = self.charges_fee

                        if ctotal_balanc >= ( self.amount + charges_fee):
                            try:                                
                                new_bal = ctotal_balanc - self.amount - charges_fee
                                # self.current_bal = new_bal
                                Account.objects.filter(user_id=self.user_id).update(balance= new_bal)
                                self.withrawned = True # transaction done

                                # else:
                                #     self.withrawned= False
                                #     raise Exception #('insufficient funds in your account')

                                try:
                                    if not self.has_record:
                                        TransactionLog.objects.create(user_id =self.user_id,amount= self.amount ,trans_type = 'Withrawal')
                                        self.has_record = True
                                        self.active = False
                                except Exception as e:
                                    print('TRANSWITH:',e)
                                    pass

                            except Exception as e:
                                print('ACCC',e)
                        # else:
                        #     return#
                                
                except Exception as e:  
                    print('CashWithRawal:',e)
                    return  # incase of error /No withrawing should happen
                    # pass
                if self.approved: #and self.withrawned and self.has_record:
                    self.active =False

                super().save(*args, **kwargs)