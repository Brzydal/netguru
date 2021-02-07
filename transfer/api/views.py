from django.http import HttpResponseRedirect
from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transfer.api.serializers import TransferSerializer, TransferPasswordSerializer, TransferDownloadSerializer
from transfer.models import Transfer


class TransferCreateAPIView(CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]


class TransferDownloadAPIView(GenericAPIView):
    serializer_class = TransferPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer_form = self.get_serializer(data=request.data)
        if not serializer_form.is_valid():
            raise ParseError(detail="No valid values")
        transfer = get_object_or_404(
            Transfer,
            url_hash=kwargs['url_hash'],
            url_password=request.data['password'],
        )
        transfer.update_counter()

        if kwargs['option'] == 'picture':
            return HttpResponseRedirect(redirect_to=transfer.get_picture_url())
        if kwargs['option'] == 'website':
            return HttpResponseRedirect(redirect_to=transfer.website)
        serializer = TransferDownloadSerializer(transfer)
        return Response(serializer.data)
