from os import environ
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db import connection
from elasticsearch import Elasticsearch


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

    @classmethod
    def update_rating(cls, product_id, rating_avg):
        update = f'UPDATE {GreatProduct._meta.db_table} SET rating = %s WHERE id=%s'
        with connection.cursor() as cursor:
            cursor.execute(update, [rating_avg, product_id])

    @classmethod
    def search(cls, search_term):
        es_client = Elasticsearch(
            f'{environ["ELASTICSEARCH_SCHEME"]}://{environ["ELASTICSEARCH_HOST"]}:{environ["ELASTICSEARCH_PORT"]}'
        )

        response = es_client.search(
            index='app_greatproduct',
            query={
                "match": {
                    "name": {
                        "query": search_term,
                        "fuzziness": "AUTO"
                    }
                }
            }
        )

        id_list = [doc['_source']['id'] for doc in response['hits']['hits']]
        return id_list


class UserRatings(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    product = models.ForeignKey(GreatProduct, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now=True, blank=True)

    objects = models.Manager()

    class Meta:
        unique_together = ['user', 'product']

    @classmethod
    def get_product_avg_rating(cls, product_id):
        result = cls.objects.filter(product__id=product_id).aggregate(Avg('rating'))
        return round(result['rating__avg'], 2)
