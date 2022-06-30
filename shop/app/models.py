from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


class GreatProduct(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))])
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('99999999.99'))])
    updated_at = models.DateTimeField(blank=True)

    objects = models.Manager()
