from hashlib import md5

from django.conf import settings
from django.db import models


class LinkModel(models.Model):
    long_url = models.CharField(max_length=10000)
    checksum = models.CharField(max_length=settings.CHECKSUM_LENGTH, primary_key=True)

    def generate_checksum(self):
        md5_obj = md5()
        md5_obj.update(self.long_url.encode('utf-8', errors='ignore'))
        long_checksum = md5_obj.hexdigest()
        short_checksum = long_checksum.upper()[:settings.CHECKSUM_LENGTH]
        self.checksum = short_checksum
        return short_checksum

    def save(self, *args, **kwargs):
        if not self.checksum:
            self.generate_checksum()
            super(LinkModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.long_url
