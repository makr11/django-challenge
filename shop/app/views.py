from django.contrib.auth.models import User, Group
from app.models import GreatProduct, UserRatings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from app.serializers import UserSerializer, GroupSerializer, GreatProductSerializer, UserRatingsSerializer


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


class GreatProductViewSet(viewsets.ModelViewSet):
    serializer_class = GreatProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'updated_at')
        order = '-' if self.request.query_params.get('order', 'asc') == "desc" else ''
        return GreatProduct.objects.all().order_by(f'{order}{order_by}')


class UserRatingsViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = UserRatingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserRatings.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        product_id = request.data.get("product")
        rating_avg = UserRatings.get_product_avg_rating(product_id)
        GreatProduct.update_rating(product_id, rating_avg)
        return response

