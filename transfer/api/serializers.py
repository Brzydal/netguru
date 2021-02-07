from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from transfer.models import Transfer


class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = ['picture', 'website', 'url_hash', 'url_password', 'is_valid']
        read_only_fields = ['url_hash', 'url_password', 'is_valid']

    def create(self, validated_data):
        user = self.context['request'].user
        transfer = Transfer.objects.create(
            created_by=user,
            **validated_data
        )
        return transfer

