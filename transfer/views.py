from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, FormView

from transfer.forms import PasswordForm, TransferCreateForm
from transfer.models import Transfer


class TransferCreate(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TransferCreateForm
    template_name = 'transfer/transfer_create_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TransferDetail(LoginRequiredMixin, DetailView):
    model = Transfer
    context_object_name = 'transfer'

    def get_object(self):
        return get_object_or_404(
            self.model,
            url_hash=self.kwargs['url_hash'],
            created_by=self.request.user
        )


class TransferPassword(FormView):
    template_name = 'transfer/password_form.html'
    form_class = PasswordForm
    success_url = 'thanks'

    def get(self, request, *args, **kwargs):
        url_hash = self.kwargs['url_hash']
        transfer = Transfer.objects.get(url_hash=url_hash)
        if not transfer.is_valid():
            return redirect('transfer-invalid')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['password']
        url_hash = self.kwargs['url_hash']
        try:
            transfer = Transfer.objects.get(url_hash=url_hash, url_password=password)
        except Transfer.DoesNotExist:
            transfer = None

        if transfer:
            transfer.update_counter()
            if transfer.picture:
                return redirect(to=transfer.get_picture_url())
            if transfer.website:
                return redirect(to=transfer.website)
            return redirect('transfer-download', url_hash=url_hash, url_password=password)
        else:
            form.add_error('password', "Incorrect password")
            return self.form_invalid(form)


class TransferDownload(DetailView):
    model = Transfer
    template_name = 'transfer/transfer_download.html'
    context_object_name = 'transfer'

    def get(self, request, *args, **kwargs):
        transfer = self.get_object()
        if not transfer.is_valid():
            return redirect('transfer-invalid')
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(
            self.model,
            url_hash=self.kwargs['url_hash'],
            url_password=self.kwargs['url_password'],
        )
