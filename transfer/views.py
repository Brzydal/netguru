from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView

from transfer.forms import PasswordForm
from transfer.models import Transfer


class TransferDetail(DetailView):
    model = Transfer
    context_object_name = 'transfer'
    slug_field = "url_hash"
    slug_url_kwarg = "url_hash"


class TransferCreate(CreateView):
    model = Transfer
    template_name = 'transfer/transfer_create_form.html'
    fields = ['website', 'picture']


class TransferPassword(FormView):
    template_name = 'transfer/password_form.html'
    form_class = PasswordForm
    success_url = 'thanks'

    def form_valid(self, form):
        password = form.cleaned_data['password']
        url_hash = self.kwargs['url_hash']
        try:
            transfer = Transfer.objects.get(url_hash=url_hash, url_password=password)
        except Transfer.DoesNotExist:
            transfer = None

        if transfer:
            transfer.update_counter()
            return redirect('transfer-download', url_hash=url_hash, url_password=password)
        else:
            return self.form_invalid(form)


class TransferDownload(DetailView):
    model = Transfer
    template_name = 'transfer/transfer_download.html'
    context_object_name = 'transfer'

    def get_object(self):
        return get_object_or_404(
            self.model,
            url_hash=self.kwargs['url_hash'],
            url_password=self.kwargs['url_password'],
        )
