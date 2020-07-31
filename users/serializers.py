
from django.contrib.auth.models import User
from .models import CustomUser ,Account
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('user_id','user',  'mobile_no',)
        read_only_fields = ('active', 'is_staff')



class UserSerializer(serializers.ModelSerializer):
    """
    A UserProfile serializer to return the UserProfile details
    """
    # profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password',)#'profile')

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
    autogen_account_no = serializers.IntegerField(read_only=True)
    class Meta:
        model = Account
        fields = ('user','number','timestamp',  'active','autogen_account_no')
        read_only_fields = ('active', 'is_staff')