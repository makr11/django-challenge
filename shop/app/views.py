from os import environ
from django.contrib.auth.models import User, Group
from app.models import GreatProduct, UserRatings
from rest_framework import viewsets, permissions, mixins, filters
from app.serializers import UserSerializer, GroupSerializer, GreatProductSerializer, UserRatingsSerializer
from elasticsearch import Elasticsearch


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FilterByProductName(filters.SearchFilter):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        es_client = Elasticsearch(
            f'{environ["ELASTICSEARCH_SCHEME"]}://{environ["ELASTICSEARCH_HOST"]}:{environ["ELASTICSEARCH_PORT"]}'
        )

        response = es_client.search(
            index='app_greatproduct',
            query={
                "match": {
                    "name": {
                        "query": search_terms[0],
                        "fuzziness": "AUTO"
                    }
                }
            }
        )

        id_list = [doc['_source']['id'] for doc in response['hits']['hits']]
        return GreatProduct.objects.filter(pk__in=id_list)


class GreatProductViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD methods on Great Products.\n
    Search by fuzzy matching is enabled.\n
    Accepts ordering on any field.
    """
    queryset = GreatProduct.objects.all()
    serializer_class = GreatProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter, FilterByProductName)

    ordering_fields = '__all__'

    ordering = ('-updated_at',)

    search_fields = ['name']


class UserRatingsViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Give product ratings, only one rating per product is allowed for specific user.
    """

    serializer_class = UserRatingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserRatings.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        product_id = request.data.get("product")
        rating_avg = UserRatings.get_product_avg_rating(product_id)
        GreatProduct.update_rating(product_id, rating_avg)
        return response
