
from django.contrib.auth.models import User
from .models import SetPasswordModel
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # try:
        #     Account.objects.update_or_create(user=user) # Create User Account on user registration/creation
        # except:
        #     pass # fail save ##no need Signals at Account app fix it/
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]



class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetPasswordModel
        fields = ('user','new_password1','new_password2')
        # read_only_fields = ('active', 'is_staff')

