from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from transfer.api.serializers import TransferSerializer
from transfer.models import Transfer


class TransferCreateAPIView(CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]
