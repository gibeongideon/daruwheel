from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Add three fields to existing Django User model.
      : daru_code  and my_code for reference
      : phone number field
    """
    my_code = models.CharField(max_length=150,blank=True,null=True)
    daru_code = models.CharField(max_length=150,help_text='Enter DADMIN if you dont have Code',blank=True,null=True)
    phone_number = models.CharField(max_length=150,unique= True, null= True,blank= True)

    def __str__(self):
        return self.username

    class Meta:
        unique_together = (['username', 'phone_number'])

    def save(self, *args, **kwargs):

      if not self.pk:
        self.my_code = 'DA'+ str(self.username).upper()
        
      super(User,self).save(*args, **kwargs)
