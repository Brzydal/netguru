from django.conf import settings
from django.db import models
from django.urls import reverse

from netguru.utils import create_hash, create_password


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Transfer(TimeStampMixin):
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    url_hash = models.CharField(max_length=32, default=create_hash, unique=True)
    url_password = models.CharField(max_length=8, default=create_password)
    correct_password_counter = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id}-{self.website}-{True if self.picture else False}'

    def get_absolute_url(self):
        return reverse('transfer-detail', kwargs={'url_hash': self.url_hash})

    def get_password_url(self):
        return settings.DOMAIN + reverse('transfer-password', kwargs={'url_hash': self.url_hash})

    def update_counter(self):
        self.correct_password_counter += 1
        self.save()
