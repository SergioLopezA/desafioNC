from django.contrib import admin
from .models import Payable, Transaction


admin.site.register(Payable)
admin.site.register(Transaction)
