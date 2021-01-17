from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Add three fields to existing Django User model.
      : daru_code  and my_code for reference
      : phone number field
    """
    my_code = models.CharField(max_length=150,blank=True,null=True)
    daru_code = models.CharField(max_length=150,default='ADMIN')
    phone_number = models.CharField(max_length=150,unique= True,blank=True,null=True)

    def __str__(self):
        return self.username

    class Meta:
        unique_together = (['username', 'phone_number'])

    # @property
    # def code_exist(self):
    #     if self.daru_code not in self.codes():
    #         return False
    #     return True
        

    # @classmethod
    # def codes(cls):
    #     codes = ['ADMIN', ]
    #     for use in cls.objects.all():
    #         codes.append(use.my_code)
    #     return codes

    def save(self, *args, **kwargs):
        if not self.pk:
            self.my_code = 'DA' + str(self.username).upper()

        #implement in form
        # try:
        #     if self.daru_code not in self.codes():
        #         return
        #     # super(User, self).save(*args, **kwargs)

        # except Exception as e:
        #     print(e)
        #     raise
        super(User, self).save(*args, **kwargs)