from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transfer.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['request'].user
        transfer = Transfer.objects.create(
            created_by=user,
            **validated_data
        )
        return transfer

    def validate(self, attrs):
        if attrs.get('website') and attrs.get('picture'):
            raise ValidationError("Only one of the fields should be filled in.")
        return attrs

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
