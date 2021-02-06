from django.views.generic import ListView
from transfer.models import Transfer


class TransferList(ListView):
    model = Transfer
