from django.views.generic import ListView, DetailView
from transfer.models import Transfer


class TransferList(ListView):
    model = Transfer
    context_object_name = 'transfers'


class TransferDetail(DetailView):
    model = Transfer
    context_object_name = 'transfer'
    slug_field = "url_hash"
    slug_url_kwarg = "url_hash"