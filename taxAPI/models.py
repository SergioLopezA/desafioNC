from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from dateutil.relativedelta import relativedelta


def a_month_from_now():
    return datetime.date.today() + relativedelta(days=30)


class Payable(models.Model):
    STATUS_CHOICES = [
        (0, 'PENDING'),
        (1, 'PAID'),
        (2, 'EXPIRED'),
    ]

    id = models.CharField(max_length=12, primary_key=True, unique=True)
    service = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    expire_date = models.DateField(default=a_month_from_now)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    barcode = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        indexes = [
            models.Index(fields=['service']),
            models.Index(fields=['status'], name=0),
        ]

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(str(self.id), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save('barcode.png', File(buffer), save=False)
        return super().save(*args, **kwargs)


class Transaction(models.Model):
    METHOD_CHOICES = [
        ('CD', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('CA', 'Cash'),
    ]

    payment_method = models.CharField(max_length=2, choices=METHOD_CHOICES)
    card_number = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    code_bar = models.ForeignKey(Payable, on_delete=models.CASCADE)
    paid_date = models.DateField(default=datetime.date.today)
