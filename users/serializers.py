
from django.contrib.auth.models import User
from users.models import *

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

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserDetail
#         fields = ('user',  'phone_number',)
#         read_only_fields = ('active', 'is_staff')