from django.contrib import admin
from .models import *
from accounts.models import *

# Register your models here.
admin.site.register(History)
admin.site.register(CustomUser)
