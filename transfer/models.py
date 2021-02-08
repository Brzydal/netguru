import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from netguru.utils import create_hash, create_password


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Transfer(TimeStampMixin):
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    url_hash = models.CharField(max_length=32, default=create_hash, unique=True)
    url_password = models.CharField(max_length=8, default=create_password)
    correct_password_counter = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, unique=False, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('transfer-detail', kwargs={'url_hash': self.url_hash})

    def get_password_url(self):
        return settings.DOMAIN + reverse('transfer-password', kwargs={'url_hash': self.url_hash})

    def get_picture_url(self):
        return f'{settings.DOMAIN}/media/{self.picture}'

    def update_counter(self):
        self.correct_password_counter += 1
        self.save()

    def is_valid(self):
        return self.created + datetime.timedelta(days=1) > now()


class UserAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=100)

