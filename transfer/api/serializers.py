from rest_framework import serializers

from transfer.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['request'].user
        transfer = Transfer.objects.create(
            created_by=user,
            **validated_data
        )
        return transfer

    class Meta:
        model = Transfer
        fields = ['picture', 'website', 'url_hash', 'url_password', 'is_valid']
        read_only_fields = ['url_hash', 'url_password', 'is_valid']


class TransferPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Please provide password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = Transfer
        fields = ['password']


class TransferDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['picture', 'website']
        read_only_fields = ['picture', 'website']
