from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class GreatProduct(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))])
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('99999999.99'))])
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class UserRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(GreatProduct, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))])
    created_at = models.DateTimeField(auto_now=True, blank=True)

    objects = models.Manager()

    class Meta:
        unique_together = ['user', 'product']
