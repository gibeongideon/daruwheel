
from .models import *
from rest_framework import serializers


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
        fields = ('user','marketinstant','marketselection','mrkt_selection','amount',)

