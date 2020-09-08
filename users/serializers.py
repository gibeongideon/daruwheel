
from django.contrib.auth.models import User
from .models import *

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
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






class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserDetail
        fields = ('user_id','user',  'mobile_no',)
        read_only_fields = ('active', 'is_staff')



# class UserSerializer(serializers.ModelSerializer):
#     """
#     A UserProfile serializer to return the UserProfile details
#     """
#     # profile = UserProfileSerializer(required=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password',)#'profile')

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = UserSerializer.create(UserSerializer(), validated_data=profile_data)
    #     user.set_password(password)
    #     user.save()
    #     userprofile = User.objects.create(user=user, **validated_data)

    #     # newlog = Log(user="Admin", action="user/create")
    #     # newlog.save()

    #     return userprofile

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     password = validated_data.pop('password')
    #     profile = instance.profile

    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()

    #     # profile.team = profile_data.get('team', profile.team)
    #     # profile.position = profile_data.get('position', profile.position)
    #     profile.mobile_no = profile_data.get('mobile_no', profile.mobile_no)
    #     # profile.customuser_profile_pic = profile_data.get('customuser_profile_pic', profile.customuser_profile_pic)

    #     # newlog = Log(user="Admin", action="user/update")
    #     # newlog.save()
    #     return instance










class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user','balance',)
        read_only_fields = ('active', 'is_staff')



class MarketInstanceSerializer(serializers.ModelSerializer):
    """
    A UserProfile serializer to return the UserProfile details
    """
    # profile = UserProfileSerializer(required=True)
    class Meta:
        model = MarketInstance
        fields = ('__all__')
        # fields = ('id', 'marketinstance', 'amount_stake_per_market', 'created_at', 'bet_expiry_time', 'closed_at',)#'profile')


class StakeSerializer(serializers.ModelSerializer):
    """
    A Stake serializer to return the UserProfile details
    """
    class Meta:
        model = Stake
        # fields = ('__all__')
        fields = ('user_stake','marketinstant','marketselection','amount',)
