from django.db import models
from django.utils import timezone
from accounts.models import *

# Create your models here.

class History(models.Model):
    keyword = models.CharField(max_length=200, blank=False, default='')
    search_result = models.CharField(max_length=200, blank=True, default='')
    search_time = models.DateTimeField(default=timezone.now)
    custom_user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name="custom_user")

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['-id']
