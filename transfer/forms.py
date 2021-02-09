from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from transfer.models import Transfer


class TransferCreateForm(ModelForm):
    class Meta:
        model = Transfer
        fields = ['website', 'picture']

    def clean(self):
        if self.cleaned_data['website'] and self.cleaned_data['picture']:
            raise ValidationError("Only one of the fields should be filled in.")
        return self.cleaned_data


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
