from collections import OrderedDict

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


class TransferStatisticsAPIView(GenericAPIView):
    queryset = Transfer.objects.exclude(correct_password_counter=0).order_by('-date')
    permission_classes = [IsAuthenticated]

    def _get_serialized_items(self, input):
        result = OrderedDict()
        for item in input:
            if result.get(str(item.date)):
                result[str(item.date)] = {
                    "files": 1 if item.picture else result.get(str(item.date)).get('files'),
                    "links": 1 if item.website else result.get(str(item.date)).get('links')
                }
            else:
                result[str(item.date)] = {
                    "files": 1 if item.picture else 0,
                    "links": 1 if item.website else 0
                }
        return result

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(self._get_serialized_items(page))

        return Response(self._get_serialized_items(queryset))
