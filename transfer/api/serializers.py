from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transfer.models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    url_hash = serializers.SerializerMethodField()

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

    def get_url_hash(self, obj):
        return obj.get_api_url()

    class Meta:
        model = Transfer
        fields = ['picture', 'website', 'url_hash', 'url_password']
        read_only_fields = ['url_hash', 'url_password']


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
