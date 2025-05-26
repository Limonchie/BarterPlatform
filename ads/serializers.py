from rest_framework import serializers
from ads.models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    ad_receiver = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('status', 'created_at')