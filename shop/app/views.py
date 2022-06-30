from django.contrib.auth.models import User, Group
from app.models import GreatProduct
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer, GroupSerializer, GreatProductSerializer


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
    queryset = GreatProduct.objects.all().order_by('-updated_at')
    serializer_class = GreatProductSerializer
    permission_classes = [permissions.IsAuthenticated]
