# reset User Passord
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


import unicodedata

# from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
# from django.contrib.auth.hashers import (
#     UNUSABLE_PASSWORD_PREFIX, identify_hasher,
# )
# from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
# from django.core.mail import EmailMultiAlternatives
# from django.template import loader
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _

class SetPasswordModel(models.Model):

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='users_pass_reset',blank =True,null=True)
    new_password1 = models.CharField(
        max_length =250,
        #l#abel=_("New password"),
        #widget=models.PasswordInput(attrs={'autocomplete': 'new-password'}),
       # strip=False,
        help_text='password'#password_validation.password_validators_help_text_html(),
    )
    new_password2 = models.CharField(
        max_length =250,
        #la#bel=_("New password confirmation"),
        #strip=False,
        #widget=models.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='confirm password'
    )

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.new_password1#cleaned_data.get('new_password1')
        password2 = self.new_password2#cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self,*args, **kwargs):
        try:

            password = self.new_password1#self.cleaned_data["new_password1"]
            self.user.set_password(password)
            # if commit:
            self.user.save()
            return #self.user
            

        except Exception as e:
            print('RESET ERROR',e)
        super().save(*args, **kwargs)
