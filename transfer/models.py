from django.db import models

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
